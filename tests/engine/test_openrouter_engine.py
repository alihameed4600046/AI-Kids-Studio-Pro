"""Tests for the OpenRouter engine."""

from __future__ import annotations

import json
from typing import Any, AsyncGenerator, Callable
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio

from src.engine.ai_engine import (
    AuthenticationError,
    EngineConfig,
    EngineState,
    GenerationRequest,
    GenerationResponse,
    RateLimitError,
)
from src.engine.openrouter_engine import OpenRouterEngine


def _make_engine(**config_overrides: Any) -> OpenRouterEngine:
    base = {
        "provider": "openrouter",
        "model": "test-model",
        "api_key": "test-api-key",
        "timeout": 5.0,
    }
    base.update(config_overrides)
    config = EngineConfig(**base)
    return OpenRouterEngine(config=config)


def _make_response(
    text: str = "Hello, world!",
    model: str = "test-model",
    tokens_used: int = 10,
    finish_reason: str = "stop",
    **extra: Any,
) -> dict[str, Any]:
    data = {
        "id": "gen-123",
        "choices": [
            {
                "message": {"role": "assistant", "content": text},
                "finish_reason": finish_reason,
            }
        ],
        "usage": {"total_tokens": tokens_used, "prompt_tokens": 5, "completion_tokens": 5},
    }
    data.update(extra)
    return data


def _make_mock_response(
    status: int = 200,
    response_data: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> Any:
    mock_response = MagicMock()
    mock_response.status = status
    mock_response.headers = headers or {}
    mock_response.text = AsyncMock(return_value=json.dumps(response_data or {}))
    mock_response.json = AsyncMock(return_value=response_data or {})
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=False)
    return mock_response


@pytest_asyncio.fixture
async def engine_factory() -> AsyncGenerator[Callable[..., OpenRouterEngine], None]:
    engines: list[OpenRouterEngine] = []

    def _create(**config_overrides: Any) -> OpenRouterEngine:
        engine = _make_engine(**config_overrides)
        engines.append(engine)
        return engine

    yield _create

    for engine in engines:
        try:
            await engine.shutdown()
        except Exception:
            pass


class TestOpenRouterEngine:
    """Tests for OpenRouterEngine."""

    @pytest.mark.asyncio
    async def test_initialize_success(self, engine_factory) -> None:
        engine = engine_factory()
        await engine.initialize()
        assert engine.state == EngineState.READY
        assert engine.is_ready

    @pytest.mark.asyncio
    async def test_initialize_missing_api_key(self, engine_factory) -> None:
        engine = engine_factory(api_key="")
        with pytest.raises(AuthenticationError, match="API key is not configured"):
            await engine.initialize()

    @pytest.mark.asyncio
    async def test_generate_success(self, engine_factory) -> None:
        engine = engine_factory()
        await engine.initialize()

        response_data = _make_response(text="Generated text", tokens_used=15)
        mock_response = _make_mock_response(200, response_data)
        mock_post = MagicMock(return_value=mock_response)

        with patch.object(engine._session, "post", mock_post):
            request = GenerationRequest(prompt="Say hello")
            response = await engine.generate(request)

        assert response.text == "Generated text"
        assert response.model == "test-model"
        assert response.provider == "openrouter"
        assert response.tokens_used == 15
        assert response.finish_reason == "stop"
        assert response.latency_ms is not None

    @pytest.mark.asyncio
    async def test_generate_model_override(self, engine_factory) -> None:
        engine = engine_factory()
        await engine.initialize()

        response_data = _make_response()
        mock_response = _make_mock_response(200, response_data)
        mock_post = MagicMock(return_value=mock_response)

        with patch.object(engine._session, "post", mock_post):
            request = GenerationRequest(prompt="Test", model="override-model")
            await engine.generate(request)

        call_args = mock_post.call_args
        payload = call_args.kwargs.get("json", call_args[1].get("json") if len(call_args) > 1 else {})
        assert payload["model"] == "override-model"

    @pytest.mark.asyncio
    async def test_generate_temperature_override(self, engine_factory) -> None:
        engine = engine_factory(temperature=0.5)
        await engine.initialize()

        response_data = _make_response()
        mock_response = _make_mock_response(200, response_data)
        mock_post = MagicMock(return_value=mock_response)

        with patch.object(engine._session, "post", mock_post):
            request = GenerationRequest(prompt="Test", temperature=0.9)
            await engine.generate(request)

        call_args = mock_post.call_args
        payload = call_args.kwargs.get("json", call_args[1].get("json") if len(call_args) > 1 else {})
        assert payload["temperature"] == 0.9

    @pytest.mark.asyncio
    async def test_generate_max_tokens_override(self, engine_factory) -> None:
        engine = engine_factory(max_tokens=100)
        await engine.initialize()

        response_data = _make_response()
        mock_response = _make_mock_response(200, response_data)
        mock_post = MagicMock(return_value=mock_response)

        with patch.object(engine._session, "post", mock_post):
            request = GenerationRequest(prompt="Test", max_tokens=500)
            await engine.generate(request)

        call_args = mock_post.call_args
        payload = call_args.kwargs.get("json", call_args[1].get("json") if len(call_args) > 1 else {})
        assert payload["max_tokens"] == 500

    @pytest.mark.asyncio
    async def test_generate_uses_config_defaults(self, engine_factory) -> None:
        engine = engine_factory(temperature=0.3, max_tokens=50)
        await engine.initialize()

        response_data = _make_response()
        mock_response = _make_mock_response(200, response_data)
        mock_post = MagicMock(return_value=mock_response)

        with patch.object(engine._session, "post", mock_post):
            request = GenerationRequest(prompt="Test")
            await engine.generate(request)

        call_args = mock_post.call_args
        payload = call_args.kwargs.get("json", call_args[1].get("json") if len(call_args) > 1 else {})
        assert payload["temperature"] == 0.3
        assert payload["max_tokens"] == 50

    @pytest.mark.asyncio
    async def test_generate_http_401_raises_auth_error(self, engine_factory) -> None:
        engine = engine_factory()
        await engine.initialize()

        response_data = {"error": {"message": "Invalid API key"}}
        mock_response = _make_mock_response(401, response_data)
        mock_post = MagicMock(return_value=mock_response)

        with patch.object(engine._session, "post", mock_post):
            request = GenerationRequest(prompt="Test")
            with pytest.raises(AuthenticationError, match="authentication failed"):
                await engine.generate(request)

    @pytest.mark.asyncio
    async def test_generate_http_429_raises_rate_limit(self, engine_factory) -> None:
        engine = engine_factory()
        await engine.initialize()

        response_data = {"error": {"message": "Rate limit exceeded", "retry_after": "60"}}
        mock_response = _make_mock_response(429, response_data)
        mock_post = MagicMock(return_value=mock_response)

        with patch.object(engine._session, "post", mock_post):
            request = GenerationRequest(prompt="Test")
            with pytest.raises(Exception, match="rate limit"):
                await engine.generate(request)

    @pytest.mark.asyncio
    async def test_generate_timeout_handling(self, engine_factory) -> None:
        engine = engine_factory()
        await engine.initialize()

        mock_post = MagicMock(side_effect=TimeoutError("Request timed out"))

        with patch.object(engine._session, "post", mock_post):
            request = GenerationRequest(prompt="Test")
            with pytest.raises(Exception, match="timed out"):
                await engine.generate(request)

    @pytest.mark.asyncio
    async def test_generate_connection_error_handling(self, engine_factory) -> None:
        engine = engine_factory()
        await engine.initialize()

        mock_post = MagicMock(side_effect=ConnectionError("Network unreachable"))

        with patch.object(engine._session, "post", mock_post):
            request = GenerationRequest(prompt="Test")
            with pytest.raises(Exception, match="Network unreachable"):
                await engine.generate(request)

    @pytest.mark.asyncio
    async def test_generate_generic_api_error(self, engine_factory) -> None:
        engine = engine_factory(max_retries=0)
        await engine.initialize()

        mock_post = MagicMock(side_effect=Exception("500 Internal Server Error"))

        with patch.object(engine._session, "post", mock_post):
            request = GenerationRequest(prompt="Test")
            with pytest.raises(Exception, match="500 Internal Server Error"):
                await engine.generate(request)

    @pytest.mark.asyncio
    async def test_api_key_not_leaked_in_logs_or_errors(self, engine_factory) -> None:
        engine = engine_factory(api_key="super-secret-key-12345", max_retries=0)
        await engine.initialize()

        mock_post = MagicMock(side_effect=Exception("401 Unauthorized"))

        with patch.object(engine._session, "post", mock_post):
            request = GenerationRequest(prompt="Test")
            try:
                await engine.generate(request)
            except Exception as exc:
                assert "super-secret-key-12345" not in str(exc)
                assert "test-api-key" not in str(exc)

    @pytest.mark.asyncio
    async def test_generate_uses_config_model_when_no_override(self, engine_factory) -> None:
        engine = engine_factory(model="configured-model")
        await engine.initialize()

        response_data = _make_response()
        mock_response = _make_mock_response(200, response_data)
        mock_post = MagicMock(return_value=mock_response)

        with patch.object(engine._session, "post", mock_post):
            request = GenerationRequest(prompt="Test")
            response = await engine.generate(request)

        assert response.model == "configured-model"

    @pytest.mark.asyncio
    async def test_model_manager_routes_to_openrouter(self, engine_factory) -> None:
        from src.engine.model_manager import ModelManager, ProviderConfig, ProviderType

        engine = engine_factory()
        await engine.initialize()

        response_data = _make_response(text="From OpenRouter")
        mock_response = _make_mock_response(200, response_data)
        mock_post = MagicMock(return_value=mock_response)

        with patch.object(engine._session, "post", mock_post):
            manager = ModelManager()
            manager.register_provider(
                ProviderConfig(
                    provider_type=ProviderType.OPENROUTER,
                    api_key="test-key",
                    enabled=True,
                    priority=1,
                    metadata={"supported_tasks": ["text_generation"]},
                )
            )
            manager.register_engine(ProviderType.OPENROUTER, engine)

            request = GenerationRequest(prompt="Hello")
            response = await manager.generate(
                request, provider_type=ProviderType.OPENROUTER
            )

        assert response.text == "From OpenRouter"
        assert response.provider == "openrouter"
