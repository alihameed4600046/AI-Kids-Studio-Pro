"""Model Manager for managing multiple AI providers.

This module provides the ModelManager class which handles multiple
AI providers including OpenRouter, Agnes AI, Google Gemini, Groq,
Edge TTS, and NexaAPI. It includes auto-fallback, rate limiting,
and quota management.
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Sequence

from src.engine.ai_engine import (
    AIEngine,
    AIEngineError,
    EngineConfig,
    GenerationRequest,
    GenerationResponse,
    RateLimitError,
)
from src.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


class ProviderType(Enum):
    """Supported AI providers."""

    OPENROUTER = "openrouter"
    AGNES_AI = "agnes_ai"
    GEMINI = "gemini"
    GROQ = "groq"
    EDGE_TTS = "edge_tts"
    NEXA_API = "nexa_api"
    MOCK = "mock"


class TaskType(Enum):
    """Types of AI tasks for provider selection."""

    TEXT_GENERATION = "text_generation"
    IMAGE_GENERATION = "image_generation"
    VIDEO_GENERATION = "video_generation"
    VOICE_GENERATION = "voice_generation"
    EMBEDDING = "embedding"


@dataclass
class ProviderConfig:
    """Configuration for a single provider."""

    provider_type: ProviderType
    api_key: str | None = None
    base_url: str | None = None
    models: list[str] = field(default_factory=list)
    rate_limit_rpm: int = 60
    rate_limit_tpm: int = 100000
    quota_requests: int = 1000
    quota_tokens: int = 1000000
    enabled: bool = True
    priority: int = 100
    timeout: float = 30.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class QuotaUsage:
    """Tracks quota usage for a provider."""

    requests_used: int = 0
    tokens_used: int = 0
    last_reset: datetime = field(default_factory=datetime.now)
    window: timedelta = field(default_factory=lambda: timedelta(hours=1))

    def should_reset(self) -> bool:
        """Check if the quota window should reset."""
        return datetime.now() - self.last_reset >= self.window

    def reset(self) -> None:
        """Reset quota counters."""
        self.requests_used = 0
        self.tokens_used = 0
        self.last_reset = datetime.now()

    def increment(self, tokens: int = 0) -> None:
        """Increment usage counters.

        Parameters
        ----------
        tokens:
            Number of tokens used in this request.
        """
        if self.should_reset():
            self.reset()
        self.requests_used += 1
        self.tokens_used += tokens

    def is_exhausted(self, provider_config: ProviderConfig) -> bool:
        """Check if quota is exhausted.

        Parameters
        ----------
        provider_config:
            Provider configuration with quota limits.

        Returns
        -------
        bool
            True if quota is exhausted.
        """
        if self.should_reset():
            return False
        return (
            self.requests_used >= provider_config.quota_requests
            or self.tokens_used >= provider_config.quota_tokens
        )


class ProviderRegistry:
    """Registry of available AI providers."""

    def __init__(self) -> None:
        self._providers: dict[ProviderType, ProviderConfig] = {}
        self._usage: dict[ProviderType, QuotaUsage] = {}
        self._rate_limiters: dict[ProviderType, list[float]] = {}

    def register(self, config: ProviderConfig) -> None:
        """Register a provider configuration.

        Parameters
        ----------
        config:
            Provider configuration.
        """
        self._providers[config.provider_type] = config
        self._usage[config.provider_type] = QuotaUsage()
        self._rate_limiters[config.provider_type] = []
        logger.info("Registered provider: %s", config.provider_type.value)

    def unregister(self, provider_type: ProviderType) -> None:
        """Unregister a provider.

        Parameters
        ----------
        provider_type:
            Provider to unregister.
        """
        self._providers.pop(provider_type, None)
        self._usage.pop(provider_type, None)
        self._rate_limiters.pop(provider_type, None)

    def get(self, provider_type: ProviderType) -> ProviderConfig | None:
        """Get provider configuration.

        Parameters
        ----------
        provider_type:
            Provider type to look up.

        Returns
        -------
        ProviderConfig | None
            Provider configuration or None if not found.
        """
        return self._providers.get(provider_type)

    def get_enabled(self) -> list[ProviderConfig]:
        """Get all enabled providers sorted by priority.

        Returns
        -------
        list[ProviderConfig]
            Sorted list of enabled providers.
        """
        return sorted(
            [p for p in self._providers.values() if p.enabled],
            key=lambda p: p.priority,
        )

    def get_usage(self, provider_type: ProviderType) -> QuotaUsage:
        """Get quota usage for a provider.

        Parameters
        ----------
        provider_type:
            Provider type.

        Returns
        -------
        QuotaUsage
            Quota usage tracker.
        """
        if provider_type not in self._usage:
            self._usage[provider_type] = QuotaUsage()
        return self._usage[provider_type]

    def is_rate_limited(self, provider_type: ProviderType) -> bool:
        """Check if a provider is currently rate limited.

        Parameters
        ----------
        provider_type:
            Provider type to check.

        Returns
        -------
        bool
            True if the provider is rate limited.
        """
        if provider_type not in self._rate_limiters:
            return False

        now = time.time()
        window = 60.0  # 1 minute window
        cutoff = now - window

        # Clean old timestamps
        self._rate_limiters[provider_type] = [
            t for t in self._rate_limiters[provider_type] if t > cutoff
        ]

        config = self._providers.get(provider_type)
        if not config:
            return False

        return len(self._rate_limiters[provider_type]) >= config.rate_limit_rpm

    def record_request(self, provider_type: ProviderType, tokens: int = 0) -> None:
        """Record a request for rate limiting and quota tracking.

        Parameters
        ----------
        provider_type:
            Provider that handled the request.
        tokens:
            Number of tokens used.
        """
        now = time.time()
        if provider_type not in self._rate_limiters:
            self._rate_limiters[provider_type] = []
        self._rate_limiters[provider_type].append(now)
        self.get_usage(provider_type).increment(tokens)


class ModelManager:
    """Manager for multiple AI providers with auto-fallback.

    This class manages multiple AI providers, handles provider selection
    based on task type, implements auto-fallback on failures, and tracks
    rate limits and quotas.

    Attributes
    ----------
    registry:
        Provider registry containing all configured providers.
    default_provider:
        Default provider to use when no preference is specified.
    """

    def __init__(self) -> None:
        self.registry = ProviderRegistry()
        self.default_provider: ProviderType | None = None
        self._engines: dict[ProviderType, AIEngine] = {}
        self._fallback_order: list[ProviderType] = []

    def register_provider(self, config: ProviderConfig) -> None:
        """Register a new provider.

        Parameters
        ----------
        config:
            Provider configuration.
        """
        self.registry.register(config)
        if self.default_provider is None and config.enabled:
            self.default_provider = config.provider_type

    def register_engine(self, provider_type: ProviderType, engine: AIEngine) -> None:
        """Register an engine instance for a provider.

        Parameters
        ----------
        provider_type:
            Provider type the engine handles.
        engine:
            Engine instance.
        """
        self._engines[provider_type] = engine
        logger.debug("Registered engine for %s", provider_type.value)

    def set_fallback_order(self, providers: Sequence[ProviderType]) -> None:
        """Set the fallback order for providers.

        Parameters
        ----------
        providers:
            Sequence of providers to try in order.
        """
        self._fallback_order = list(providers)
        logger.info("Fallback order set: %s", [p.value for p in providers])

    def get_provider_for_task(self, task_type: TaskType) -> ProviderConfig | None:
        """Select the best provider for a given task type.

        Parameters
        ----------
        task_type:
            Type of AI task.

        Returns
        -------
        ProviderConfig | None
            Best provider for the task, or None if no suitable provider.
        """
        enabled = self.registry.get_enabled()
        if not enabled:
            return None

        # Filter providers that support the task type
        suitable = []
        for provider in enabled:
            if task_type.value in provider.metadata.get("supported_tasks", []):
                if not self.registry.is_rate_limited(provider.provider_type):
                    usage = self.registry.get_usage(provider.provider_type)
                    if not usage.is_exhausted(provider):
                        suitable.append(provider)

        if not suitable:
            return enabled[0] if enabled else None

        return min(suitable, key=lambda p: p.priority)

    async def generate(
        self,
        request: GenerationRequest,
        provider_type: ProviderType | None = None,
        task_type: TaskType = TaskType.TEXT_GENERATION,
        fallback: bool = True,
    ) -> GenerationResponse:
        """Generate a response using the best available provider.

        Parameters
        ----------
        request:
            Generation request.
        provider_type:
            Specific provider to use. If None, auto-select.
        task_type:
            Type of task for provider selection.
        fallback:
            Whether to try fallback providers on failure.

        Returns
        -------
        GenerationResponse
            Generated response.

        Raises
        ------
        AIEngineError
            If all providers fail.
        """
        providers_to_try = []

        if provider_type:
            providers_to_try = [provider_type]
        else:
            selected = self.get_provider_for_task(task_type)
            if selected:
                providers_to_try = [selected.provider_type]
            if fallback and self._fallback_order:
                providers_to_try.extend(
                    p for p in self._fallback_order if p not in providers_to_try
                )

        last_error: Exception | None = None
        for prov in providers_to_try:
            try:
                return await self._generate_with_provider(prov, request)
            except (RateLimitError, AIEngineError) as exc:
                last_error = exc
                logger.warning(
                    "Provider %s failed: %s. Trying next provider...",
                    prov.value,
                    str(exc),
                )
                continue
            except Exception as exc:
                last_error = exc
                logger.error("Unexpected error with %s: %s", prov.value, str(exc))
                continue

        raise AIEngineError(
            f"All providers failed. Last error: {last_error}",
            provider=provider_type.value if provider_type else None,
        ) from last_error

    async def _generate_with_provider(
        self,
        provider_type: ProviderType,
        request: GenerationRequest,
    ) -> GenerationResponse:
        """Generate using a specific provider.

        Parameters
        ----------
        provider_type:
            Provider to use.
        request:
            Generation request.

        Returns
        -------
        GenerationResponse
            Generated response.

        Raises
        ------
        AIEngineError
            If generation fails.
        """
        if self.registry.is_rate_limited(provider_type):
            raise RateLimitError(
                f"Provider {provider_type.value} is rate limited",
                provider=provider_type.value,
            )

        engine = self._engines.get(provider_type)
        if not engine:
            raise AIEngineError(
                f"No engine registered for provider {provider_type.value}",
                provider=provider_type.value,
            )

        if not engine.is_ready:
            try:
                await engine.initialize()
            except AIEngineError as exc:
                raise AIEngineError(
                    f"Failed to initialize {provider_type.value}: {exc}",
                    provider=provider_type.value,
                ) from exc

        start_time = time.time()
        try:
            response = await engine.generate(request)
            latency = (time.time() - start_time) * 1000
            response.latency_ms = latency
            self.registry.record_request(
                provider_type,
                tokens=response.tokens_used or 0,
            )
            logger.info(
                "Generated response with %s in %.0fms",
                provider_type.value,
                latency,
            )
            return response
        except AIEngineError:
            raise
        except Exception as exc:
            raise AIEngineError(
                f"Generation failed with {provider_type.value}: {exc}",
                provider=provider_type.value,
            ) from exc

    async def stream(
        self,
        request: GenerationRequest,
        provider_type: ProviderType | None = None,
    ) -> AsyncGenerator[str, None]:
        """Stream a response from the best available provider.

        Parameters
        ----------
        request:
            Generation request.
        provider_type:
            Specific provider to use.

        Yields
        ------
        str
            Response chunks.
        """
        if provider_type is None:
            provider_type = self.default_provider

        if provider_type is None:
            raise AIEngineError("No provider specified and no default set")

        engine = self._engines.get(provider_type)
        if not engine:
            raise AIEngineError(
                f"No engine registered for provider {provider_type.value}",
                provider=provider_type.value,
            )

        async for chunk in engine.stream(request):
            yield chunk

    def get_available_providers(self) -> list[str]:
        """Get list of available provider names.

        Returns
        -------
        list[str]
            List of provider names.
        """
        return [p.provider_type.value for p in self.registry.get_enabled()]

    def get_provider_status(self) -> dict[str, dict[str, Any]]:
        """Get status of all registered providers.

        Returns
        -------
        dict[str, dict[str, Any]]
            Status information for each provider.
        """
        status = {}
        for prov, config in self.registry._providers.items():
            usage = self.registry.get_usage(prov)
            engine = self._engines.get(prov)
            status[prov.value] = {
                "enabled": config.enabled,
                "priority": config.priority,
                "requests_used": usage.requests_used,
                "tokens_used": usage.tokens_used,
                "rate_limited": self.registry.is_rate_limited(prov),
                "engine_ready": engine.is_ready if engine else False,
                "quota_remaining": max(
                    0, config.quota_requests - usage.requests_used
                ),
            }
        return status
