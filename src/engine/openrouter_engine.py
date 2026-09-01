"""OpenRouter AI text generation engine.

This module provides the OpenRouterEngine class which integrates
OpenRouter's text generation API with the existing AI engine architecture.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from typing import Any, AsyncGenerator

import aiohttp

from src.engine.ai_engine import (
    AIEngine,
    AIEngineError,
    AuthenticationError,
    EngineConfig,
    EngineState,
    GenerationRequest,
    GenerationResponse,
    RateLimitError,
)
from src.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


class OpenRouterEngine(AIEngine):
    """OpenRouter text generation engine.

    This engine sends text generation requests to OpenRouter's API
    and returns the generated text as a GenerationResponse.

    Attributes
    ----------
    base_url:
        OpenRouter API base URL.
    """

    DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"
    DEFAULT_MODEL = "openai/gpt-3.5-turbo"

    def __init__(self, config: EngineConfig | None = None) -> None:
        if config is None:
            config = EngineConfig(
                provider="openrouter",
                model=self.DEFAULT_MODEL,
                api_key=None,
                timeout=30.0,
            )
        super().__init__(config)
        self.base_url = self._config.metadata.get("base_url", self.DEFAULT_BASE_URL)
        self._session: aiohttp.ClientSession | None = None

    async def initialize(self) -> None:
        """Initialize the OpenRouter engine.

        Validates that an API key is available. Does not make an
        expensive generation request.

        Raises
        ------
        AuthenticationError
            If no API key is configured.
        AIEngineError
            If initialization fails.
        """
        self._state = EngineState.LOADING
        logger.info("Initializing OpenRouter engine...")

        api_key = self._config.api_key
        if not api_key:
            raise AuthenticationError(
                "OpenRouter API key is not configured.",
                provider=self._config.provider,
            )

        self._session = aiohttp.ClientSession()
        self._state = EngineState.READY
        logger.info("OpenRouter engine initialized")

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        """Generate text using OpenRouter.

        Parameters
        ----------
        request:
            Generation request containing prompt and options.

        Returns
        -------
        GenerationResponse
            Generated response with text, model, provider, token usage,
            and finish reason.

        Raises
        ------
        EngineNotReadyError
            If the engine is not initialized.
        AuthenticationError
            If authentication fails (HTTP 401/403).
        RateLimitError
            If rate limit is hit (HTTP 429).
        AIEngineError
            For other API/network failures.
        """
        if self._state != EngineState.READY:
            raise EngineNotReadyError(
                f"OpenRouter engine is not ready (state={self._state.value})",
                provider=self._config.provider,
            )

        self._state = EngineState.GENERATING
        start_time = time.time()

        try:
            response = await self._execute_with_retry(
                self._send_generation_request, request
            )
            latency = (time.time() - start_time) * 1000
            self._record_success()
            self._state = EngineState.READY
            response.latency_ms = latency
            return response
        except AIEngineError:
            self._record_error(AIEngineError("OpenRouter generation failed"))
            self._state = EngineState.ERROR
            raise
        except Exception as exc:
            self._record_error(AIEngineError(f"OpenRouter generation failed: {exc}"))
            self._state = EngineState.ERROR
            raise AIEngineError(
                f"OpenRouter generation failed: {exc}",
                provider=self._config.provider,
            ) from exc

    async def _send_generation_request(
        self, request: GenerationRequest
    ) -> GenerationResponse:
        """Send the actual HTTP request to OpenRouter.

        Parameters
        ----------
        request:
            Generation request.

        Returns
        -------
        GenerationResponse
            Parsed response from OpenRouter.

        Raises
        ------
        AuthenticationError
            If HTTP 401/403 is returned.
        RateLimitError
            If HTTP 429 is returned.
        AIEngineError
            For other HTTP/API failures.
        """
        if self._session is None:
            raise AIEngineError(
                "OpenRouter engine session not initialized",
                provider=self._config.provider,
            )

        model = request.model or self._config.model
        temperature = request.temperature if request.temperature is not None else self._config.temperature
        max_tokens = request.max_tokens if request.max_tokens is not None else self._config.max_tokens

        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": request.prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        headers = {
            "Authorization": f"Bearer {self._config.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ai-kids-studio-pro.local",
            "X-Title": "AI Kids Studio Pro",
        }

        url = f"{self.base_url}/chat/completions"

        try:
            async with self._session.post(
                url,
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self._config.timeout),
            ) as http_response:
                status = http_response.status
                response_text = await http_response.text()

                if status in (401, 403):
                    raise AuthenticationError(
                        "OpenRouter authentication failed.",
                        provider=self._config.provider,
                    )
                if status == 429:
                    retry_after = None
                    try:
                        error_data = json.loads(response_text)
                        retry_after = error_data.get("error", {}).get("retry_after")
                    except (json.JSONDecodeError, AttributeError):
                        pass
                    raise RateLimitError(
                        "OpenRouter rate limit exceeded.",
                        retry_after=float(retry_after) if retry_after else None,
                        provider=self._config.provider,
                    )

                if status != 200:
                    raise AIEngineError(
                        f"OpenRouter API error {status}: {response_text[:200]}",
                        provider=self._config.provider,
                    )

                try:
                    data = json.loads(response_text)
                except json.JSONDecodeError as exc:
                    raise AIEngineError(
                        f"Invalid JSON response from OpenRouter: {exc}",
                        provider=self._config.provider,
                    ) from exc

                return self._parse_response(data, model)

        except aiohttp.ClientResponseError as exc:
            if exc.status in (401, 403):
                raise AuthenticationError(
                    "OpenRouter authentication failed.",
                    provider=self._config.provider,
                ) from exc
            if exc.status == 429:
                raise RateLimitError(
                    "OpenRouter rate limit exceeded.",
                    provider=self._config.provider,
                ) from exc
            raise AIEngineError(
                f"OpenRouter API error: {exc}",
                provider=self._config.provider,
            ) from exc
        except aiohttp.ClientConnectionError as exc:
            raise AIEngineError(
                f"Connection to OpenRouter failed: {exc}",
                provider=self._config.provider,
            ) from exc
        except asyncio.TimeoutError as exc:
            raise AIEngineError(
                "OpenRouter request timed out.",
                provider=self._config.provider,
            ) from exc

    def _parse_response(self, data: dict[str, Any], model: str) -> GenerationResponse:
        """Parse OpenRouter API response into GenerationResponse.

        Parameters
        ----------
        data:
            Parsed JSON response from OpenRouter.
        model:
            Model name used for the request.

        Returns
        -------
        GenerationResponse
            Parsed generation response.

        Raises
        ------
        AIEngineError
            If the response format is invalid.
        """
        try:
            choices = data.get("choices", [])
            if not choices:
                raise AIEngineError(
                    "OpenRouter returned no choices in response.",
                    provider=self._config.provider,
                )

            message = choices[0].get("message", {})
            text = message.get("content", "")
            if not text:
                text = choices[0].get("text", "")

            finish_reason = choices[0].get("finish_reason")

            usage = data.get("usage", {})
            tokens_used = usage.get("total_tokens")

            return GenerationResponse(
                text=text,
                model=model,
                provider=self._config.provider,
                tokens_used=tokens_used,
                finish_reason=finish_reason,
                metadata={
                    "openrouter_id": data.get("id"),
                    "usage": usage,
                },
            )
        except AIEngineError:
            raise
        except Exception as exc:
            raise AIEngineError(
                f"Failed to parse OpenRouter response: {exc}",
                provider=self._config.provider,
            ) from exc

    async def stream(
        self, request: GenerationRequest
    ) -> AsyncGenerator[str, None]:
        """Stream a response from OpenRouter.

        Parameters
        ----------
        request:
            Generation request.

        Yields
        ------
        str
            Response chunks.

        Raises
        ------
        EngineNotReadyError
            If the engine is not initialized.
        AIEngineError
            If streaming fails.
        """
        if self._state != EngineState.READY:
            raise EngineNotReadyError(
                f"OpenRouter engine is not ready (state={self._state.value})",
                provider=self._config.provider,
            )

        self._state = EngineState.GENERATING
        try:
            response = await self._send_streaming_request(request)
            self._record_success()
            self._state = EngineState.READY
            async for chunk in response:
                yield chunk
        except AIEngineError:
            self._record_error(AIEngineError("OpenRouter streaming failed"))
            self._state = EngineState.ERROR
            raise
        except Exception as exc:
            self._record_error(AIEngineError(f"OpenRouter streaming failed: {exc}"))
            self._state = EngineState.ERROR
            raise AIEngineError(
                f"OpenRouter streaming failed: {exc}",
                provider=self._config.provider,
            ) from exc

    async def _send_streaming_request(
        self, request: GenerationRequest
    ) -> AsyncGenerator[str, None]:
        """Send a streaming request to OpenRouter.

        Parameters
        ----------
        request:
            Generation request.

        Yields
        ------
        str
            Response chunks.

        Raises
        ------
        AIEngineError
            If the streaming request fails.
        """
        if self._session is None:
            raise AIEngineError(
                "OpenRouter engine session not initialized",
                provider=self._config.provider,
            )

        model = request.model or self._config.model
        temperature = request.temperature if request.temperature is not None else self._config.temperature
        max_tokens = request.max_tokens if request.max_tokens is not None else self._config.max_tokens

        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": request.prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }

        headers = {
            "Authorization": f"Bearer {self._config.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ai-kids-studio-pro.local",
            "X-Title": "AI Kids Studio Pro",
        }

        url = f"{self.base_url}/chat/completions"

        try:
            async with self._session.post(
                url,
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self._config.timeout),
            ) as http_response:
                if http_response.status in (401, 403):
                    raise AuthenticationError(
                        "OpenRouter authentication failed.",
                        provider=self._config.provider,
                    )
                if http_response.status == 429:
                    raise RateLimitError(
                        "OpenRouter rate limit exceeded.",
                        provider=self._config.provider,
                    )

                async for line in http_response.content:
                    line = line.decode("utf-8").strip()
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str == "[DONE]":
                            break
                        try:
                            chunk_data = json.loads(data_str)
                            delta = chunk_data.get("choices", [{}])[0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                yield content
                        except (json.JSONDecodeError, IndexError, KeyError):
                            continue
        except aiohttp.ClientConnectionError as exc:
            raise AIEngineError(
                f"Connection to OpenRouter failed: {exc}",
                provider=self._config.provider,
            ) from exc
        except asyncio.TimeoutError as exc:
            raise AIEngineError(
                "OpenRouter streaming request timed out.",
                provider=self._config.provider,
            ) from exc

    async def validate(self) -> bool:
        """Validate the OpenRouter engine.

        Returns
        -------
        bool
            True if the engine is ready and has an API key configured.
        """
        if self._state != EngineState.READY:
            return False
        return bool(self._config.api_key)

    async def shutdown(self) -> None:
        """Shutdown the engine and release resources."""
        if self._session and not self._session.closed:
            await self._session.close()
        self._session = None
        self._state = EngineState.IDLE
        logger.info("OpenRouter engine shut down")

    @classmethod
    def from_settings(
        cls,
        settings_manager: Any = None,
        **kwargs: Any,
    ) -> OpenRouterEngine:
        """Create an OpenRouterEngine from application settings.

        Parameters
        ----------
        settings_manager:
            SettingsManager instance. If None, a new one is created.
        **kwargs:
            Additional EngineConfig overrides.

        Returns
        -------
        OpenRouterEngine
            Configured engine instance.
        """
        if settings_manager is None:
            from src.settings.manager import SettingsManager
            settings_manager = SettingsManager("config/settings.json")

        api_key = settings_manager.get("openrouter_api_key") or kwargs.pop("api_key", None)
        model = settings_manager.get("openrouter_model", cls.DEFAULT_MODEL)
        base_url = settings_manager.get("openrouter_base_url", cls.DEFAULT_BASE_URL)

        config = EngineConfig(
            provider="openrouter",
            model=model,
            api_key=api_key,
            metadata={"base_url": base_url},
            **kwargs,
        )
        return cls(config=config)
