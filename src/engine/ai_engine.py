"""Abstract AI Engine base class.

This module defines the interface that all AI engine implementations
must follow. It provides common error handling, retry logic, and
configuration patterns.
"""

from __future__ import annotations

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, AsyncGenerator, Sequence

from src.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


class EngineState(Enum):
    """Possible states for an AI engine."""

    IDLE = "idle"
    LOADING = "loading"
    READY = "ready"
    GENERATING = "generating"
    ERROR = "error"
    DISABLED = "disabled"


class RetryStrategy(Enum):
    """Retry strategies for handling transient failures."""

    NONE = "none"
    FIXED_DELAY = "fixed_delay"
    EXPONENTIAL_BACKOFF = "exponential_backoff"


@dataclass
class EngineConfig:
    """Configuration for an AI engine instance."""

    provider: str = "openrouter"
    model: str = "default"
    api_key: str | None = None
    timeout: float = 30.0
    max_retries: int = 3
    retry_strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF
    retry_delay: float = 1.0
    temperature: float = 0.7
    max_tokens: int = 2000
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if self.timeout <= 0:
            raise ValueError("timeout must be positive")
        if self.temperature < 0 or self.temperature > 2:
            raise ValueError("temperature must be between 0 and 2")
        if self.max_tokens < 1:
            raise ValueError("max_tokens must be positive")


@dataclass
class GenerationRequest:
    """Request object for AI generation."""

    prompt: str
    context: dict[str, Any] | None = None
    model: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    stream: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class GenerationResponse:
    """Response object from AI generation."""

    text: str
    model: str
    provider: str
    tokens_used: int | None = None
    finish_reason: str | None = None
    latency_ms: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class AIEngineError(Exception):
    """Base exception for AI engine errors."""

    def __init__(self, message: str, provider: str | None = None) -> None:
        super().__init__(message)
        self.provider = provider


class EngineNotReadyError(AIEngineError):
    """Raised when the engine is not ready to generate."""

    pass


class RateLimitError(AIEngineError):
    """Raised when the provider rate limit is hit."""

    def __init__(self, message: str, retry_after: float | None = None, provider: str | None = None) -> None:
        super().__init__(message, provider=provider)
        self.retry_after = retry_after


class AuthenticationError(AIEngineError):
    """Raised when authentication with the provider fails."""

    pass


class ContentFilterError(AIEngineError):
    """Raised when content is filtered by the provider."""

    pass


class AIEngine(ABC):
    """Abstract base class for AI engine implementations.

    All concrete AI engines must inherit from this class and implement
    the abstract methods. The base class provides common functionality
    such as state management, retry logic, and logging.
    """

    def __init__(self, config: EngineConfig | None = None) -> None:
        self._config = config or EngineConfig()
        self._state = EngineState.IDLE
        self._request_count = 0
        self._error_count = 0
        self._last_error: Exception | None = None
        self._start_time = time.time()

    @property
    def config(self) -> EngineConfig:
        """Return the engine configuration."""
        return self._config

    @property
    def state(self) -> EngineState:
        """Return the current engine state."""
        return self._state

    @property
    def is_ready(self) -> bool:
        """Check if the engine is ready for generation."""
        return self._state == EngineState.READY

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the engine and verify connectivity.

        Raises
        ------
        AIEngineError
            If initialization fails.
        """
        self._state = EngineState.LOADING
        logger.info("Initializing %s engine...", self.__class__.__name__)

    @abstractmethod
    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        """Generate a response for the given request.

        Parameters
        ----------
        request:
            The generation request containing prompt and options.

        Returns
        -------
        GenerationResponse
            The generated response.

        Raises
        ------
        EngineNotReadyError
            If the engine is not initialized.
        AIEngineError
            If generation fails after retries.
        """
        if self._state != EngineState.READY:
            raise EngineNotReadyError(
                f"Engine {self.__class__.__name__} is not ready (state={self._state.value})",
                provider=self._config.provider,
            )

    @abstractmethod
    async def stream(self, request: GenerationRequest) -> AsyncGenerator[str, None]:
        """Stream a response for the given request.

        Parameters
        ----------
        request:
            The generation request containing prompt and options.

        Yields
        ------
        str
            Chunks of the generated response.

        Raises
        ------
        EngineNotReadyError
            If the engine is not initialized.
        AIEngineError
            If streaming fails after retries.
        """
        if self._state != EngineState.READY:
            raise EngineNotReadyError(
                f"Engine {self.__class__.__name__} is not ready (state={self._state.value})",
                provider=self._config.provider,
            )

    @abstractmethod
    async def validate(self) -> bool:
        """Validate the engine configuration and connectivity.

        Returns
        -------
        bool
            True if the engine is valid and ready, False otherwise.
        """
        return self._state == EngineState.READY

    async def shutdown(self) -> None:
        """Shutdown the engine and release resources."""
        logger.info("Shutting down %s engine...", self.__class__.__name__)
        self._state = EngineState.IDLE

    def _record_success(self) -> None:
        """Record a successful request."""
        self._request_count += 1
        if self._state == EngineState.ERROR:
            self._state = EngineState.READY

    def _record_error(self, error: Exception) -> None:
        """Record a failed request."""
        self._error_count += 1
        self._last_error = error
        self._state = EngineState.ERROR
        logger.error("Engine error: %s", str(error), exc_info=True)

    async def _execute_with_retry(self, operation: Any, *args: Any, **kwargs: Any) -> Any:
        """Execute an operation with retry logic.

        Parameters
        ----------
        operation:
            Callable to execute.
        *args:
            Positional arguments for the operation.
        **kwargs:
            Keyword arguments for the operation.

        Returns
        -------
        Any
            Result of the operation.

        Raises
        ------
        AIEngineError
            If all retries fail.
        """
        last_exception: Exception | None = None
        retries = self._config.max_retries

        for attempt in range(retries + 1):
            try:
                return await operation(*args, **kwargs)
            except (RateLimitError, ConnectionError, TimeoutError) as exc:
                last_exception = exc
                if attempt < retries:
                    delay = self._compute_delay(attempt)
                    logger.warning(
                        "Attempt %d/%d failed: %s. Retrying in %.1fs...",
                        attempt + 1,
                        retries + 1,
                        str(exc),
                        delay,
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error("All %d attempts failed.", retries + 1)
            except AIEngineError:
                raise
            except Exception as exc:
                logger.error("Unexpected error: %s", str(exc), exc_info=True)
                raise AIEngineError(str(exc), provider=self._config.provider) from exc

        raise AIEngineError(
            f"Operation failed after {retries + 1} attempts: {last_exception}",
            provider=self._config.provider,
        ) from last_exception

    def _compute_delay(self, attempt: int) -> float:
        """Compute retry delay based on strategy.

        Parameters
        ----------
        attempt:
            Current attempt number (0-indexed).

        Returns
        -------
        float
            Delay in seconds.
        """
        if self._config.retry_strategy == RetryStrategy.NONE:
            return 0.0
        if self._config.retry_strategy == RetryStrategy.FIXED_DELAY:
            return self._config.retry_delay
        # Exponential backoff
        return self._config.retry_delay * (2**attempt)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"provider={self._config.provider!r}, "
            f"model={self._config.model!r}, "
            f"state={self._state.value})"
        )
