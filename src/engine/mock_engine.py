"""Mock AI Engine for testing and development.

This module provides mock implementations of the AI engine interface
for testing purposes. It simulates different scenarios without making
actual API calls.
"""

from __future__ import annotations

import asyncio
import logging
import random
from collections.abc import AsyncGenerator
from enum import Enum
from typing import Any

from src.engine.ai_engine import (
    AIEngine,
    AIEngineError,
    AuthenticationError,
    ContentFilterError,
    EngineConfig,
    EngineState,
    GenerationRequest,
    GenerationResponse,
    RateLimitError,
)
from src.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


class MockScenario(Enum):
    """Predefined mock scenarios for testing."""

    SUCCESS = "success"
    RATE_LIMIT = "rate_limit"
    AUTH_ERROR = "auth_error"
    TIMEOUT = "timeout"
    CONTENT_FILTER = "content_filter"
    STREAM_SUCCESS = "stream_success"
    VALIDATION_FAIL = "validation_fail"


class MockEngine(AIEngine):
    """Mock implementation of AIEngine for testing.

    This engine simulates AI generation without making actual API calls.
    It supports various scenarios for testing error handling and retry logic.

    Attributes
    ----------
    scenario:
        Current mock scenario to simulate.
    response_text:
        Custom response text to return.
    latency_ms:
        Simulated latency in milliseconds.
    """

    def __init__(self, config: EngineConfig | None = None) -> None:
        if config is None:
            config = EngineConfig(provider="mock", model="mock-model")
        super().__init__(config)
        self.scenario = MockScenario.SUCCESS
        self.response_text = "This is a mock response from the AI engine."
        self.latency_ms: float = 100.0
        self._stream_chunks: list[str] = [
            "This ", "is ", "a ", "mock ", "response ", "from ", "the ", "AI ", "engine."
        ]
        self._call_count = 0

    async def initialize(self) -> None:
        """Initialize the mock engine."""
        await asyncio.sleep(0.01)
        self._state = EngineState.READY
        logger.info("Mock engine initialized")

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        """Generate a mock response.

        Parameters
        ----------
        request:
            Generation request.

        Returns
        -------
        GenerationResponse
            Mock generated response.

        Raises
        ------
        AIEngineError
            If the mock scenario simulates an error.
        """
        self._state = EngineState.GENERATING

        try:
            await asyncio.sleep(self.latency_ms / 1000.0)
            response = await self._execute_with_retry(self._mock_generate, request)
            self._record_success()
            self._state = EngineState.READY
            return response
        except AIEngineError:
            self._record_error(AIEngineError("Mock generation failed"))
            self._state = EngineState.ERROR
            raise

    async def _mock_generate(self, request: GenerationRequest) -> GenerationResponse:
        """Internal mock generation logic.

        Parameters
        ----------
        request:
            Generation request.

        Returns
        -------
        GenerationResponse
            Mock response.

        Raises
        ------
        AIEngineError
            If the scenario simulates an error.
        """
        self._call_count += 1
        if self.scenario == MockScenario.RATE_LIMIT:
            raise RateLimitError(
                "Mock rate limit exceeded",
                retry_after=60.0,
                provider=self._config.provider,
            )
        if self.scenario == MockScenario.AUTH_ERROR:
            raise AuthenticationError(
                "Mock authentication failed",
                provider=self._config.provider,
            )
        if self.scenario == MockScenario.TIMEOUT:
            raise TimeoutError("Mock timeout")
        if self.scenario == MockScenario.CONTENT_FILTER:
            raise ContentFilterError(
                "Mock content filtered",
                provider=self._config.provider,
            )
        if self.scenario == MockScenario.VALIDATION_FAIL:
            raise AIEngineError("Mock validation failed", provider=self._config.provider)

        # Default success scenario
        prompt_length = len(request.prompt)
        tokens_used = max(1, prompt_length // 4)

        return GenerationResponse(
            text=self.response_text,
            model=request.model or self._config.model,
            provider=self._config.provider,
            tokens_used=tokens_used,
            finish_reason="stop",
            latency_ms=self.latency_ms,
            metadata={
                "mock": True,
                "call_count": self._call_count,
                "scenario": self.scenario.value,
            },
        )

    async def stream(self, request: GenerationRequest) -> AsyncGenerator[str, None]:
        """Stream a mock response.

        Parameters
        ----------
        request:
            Generation request.

        Yields
        ------
        str
            Chunks of the mock response.
        """
        self._call_count += 1
        self._state = EngineState.GENERATING

        try:
            if self.scenario == MockScenario.STREAM_SUCCESS:
                for chunk in self._stream_chunks:
                    await asyncio.sleep(0.05)
                    yield chunk
            else:
                await asyncio.sleep(self.latency_ms / 1000.0)
                yield self.response_text

            self._record_success()
            self._state = EngineState.READY
        except Exception as exc:
            self._record_error(AIEngineError(f"Mock stream failed: {exc}"))
            self._state = EngineState.ERROR
            raise

    async def validate(self) -> bool:
        """Validate the mock engine.

        Returns
        -------
        bool
            Always True for mock engine.
        """
        return self._state == EngineState.READY

    def set_scenario(self, scenario: MockScenario) -> None:
        """Set the mock scenario.

        Parameters
        ----------
        scenario:
            Scenario to simulate.
        """
        self.scenario = scenario
        logger.info("Mock scenario set to: %s", scenario.value)

    def set_response(self, text: str) -> None:
        """Set the mock response text.

        Parameters
        ----------
        text:
            Response text to return.
        """
        self.response_text = text

    def set_stream_chunks(self, chunks: list[str]) -> None:
        """Set the chunks for stream responses.

        Parameters
        ----------
        chunks:
            List of text chunks to stream.
        """
        self._stream_chunks = chunks

    def reset(self) -> None:
        """Reset the mock engine state."""
        self._call_count = 0
        self._state = EngineState.READY
        self.scenario = MockScenario.SUCCESS
        self._last_error = None
        logger.info("Mock engine reset")

    @property
    def call_count(self) -> int:
        """Return the number of times generate/stream has been called."""
        return self._call_count


class MockModelManager:
    """Mock model manager for integration testing.

    This class provides a simplified model manager that uses only
    mock engines for testing purposes.
    """

    def __init__(self) -> None:
        self.mock_engine = MockEngine()
        self.providers: list[str] = ["mock"]

    async def initialize(self) -> None:
        """Initialize all mock providers."""
        await self.mock_engine.initialize()

    async def generate(
        self, request: GenerationRequest, **kwargs: Any
    ) -> GenerationResponse:
        """Generate using the mock engine.

        Parameters
        ----------
        request:
            Generation request.
        **kwargs:
            Ignored keyword arguments.

        Returns
        -------
        GenerationResponse
            Mock response.
        """
        return await self.mock_engine.generate(request)

    async def stream(
        self, request: GenerationRequest, **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        """Stream using the mock engine.

        Parameters
        ----------
        request:
            Generation request.
        **kwargs:
            Ignored keyword arguments.

        Yields
        ------
        str
            Response chunks.
        """
        async for chunk in self.mock_engine.stream(request):
            yield chunk

    def set_scenario(self, scenario: MockScenario) -> None:
        """Set the mock scenario.

        Parameters
        ----------
        scenario:
            Scenario to simulate.
        """
        self.mock_engine.set_scenario(scenario)

    def reset(self) -> None:
        """Reset the mock manager."""
        self.mock_engine.reset()

    def get_status(self) -> dict[str, Any]:
        """Get mock manager status.

        Returns
        -------
        dict[str, Any]
            Status information.
        """
        return {
            "provider": "mock",
            "state": self.mock_engine.state.value,
            "call_count": self.mock_engine.call_count,
            "scenario": self.mock_engine.scenario.value,
        }
