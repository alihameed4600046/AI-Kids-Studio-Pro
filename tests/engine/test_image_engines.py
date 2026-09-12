"""Tests for image generation engine implementations."""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.engine.ai_engine import (
    AIEngineError,
    AuthenticationError,
    ContentFilterError,
    EngineConfig,
    EngineState,
    GenerationRequest,
    GenerationResponse,
    RateLimitError,
)
from src.engine.image_engine import (
    AgnesImageEngine,
    FluxEngine,
    SDXLEngine,
)


def _make_http_response(
    status: int = 200,
    json_data: dict[str, Any] | None = None,
    text_data: str | None = None,
    read_data: bytes = b"",
) -> MagicMock:
    """Create a mock aiohttp response object usable as an async context manager."""
    response = MagicMock()
    response.status = status
    if json_data is not None:
        response.json = AsyncMock(return_value=json_data)
    if text_data is not None:
        response.text = AsyncMock(return_value=text_data)
    response.read = AsyncMock(return_value=read_data)
    response.__aenter__ = AsyncMock(return_value=response)
    response.__aexit__ = AsyncMock(return_value=False)
    return response


def _make_mock_session(
    post_responses: list[MagicMock] | None = None,
    get_responses: list[MagicMock] | None = None,
) -> MagicMock:
    """Create a mock aiohttp.ClientSession that yields *mock_session* as an async context manager."""
    session = MagicMock()
    session.__aenter__ = AsyncMock(return_value=session)
    session.__aexit__ = AsyncMock(return_value=False)

    _post_responses = list(post_responses or [])
    _get_responses = list(get_responses or [])

    def _post(*_args: Any, **_kwargs: Any) -> MagicMock:
        if _post_responses:
            return _post_responses.pop(0)
        return _make_http_response(404)

    def _get(*_args: Any, **_kwargs: Any) -> MagicMock:
        if _get_responses:
            return _get_responses.pop(0)
        return _make_http_response(404)

    session.post = MagicMock(side_effect=_post)
    session.get = MagicMock(side_effect=_get)
    return session


class TestFluxEngine:
    """Tests for FluxEngine (NexaAPI)."""

    def _make_engine(self, **overrides: Any) -> FluxEngine:
        config = EngineConfig(
            provider="nexa_api",
            model="flux-schnell",
            api_key="test-nexa-key",
            timeout=5.0,
        )
        for k, v in overrides.items():
            setattr(config, k, v)
        return FluxEngine(config=config)

    @pytest.mark.asyncio
    async def test_initialize_success(self) -> None:
        engine = self._make_engine()
        await engine.initialize()
        assert engine.state == EngineState.READY
        assert engine.is_ready

    @pytest.mark.asyncio
    async def test_initialize_logs_warning_without_api_key(self) -> None:
        engine = self._make_engine(api_key=None)
        await engine.initialize()
        assert engine.state == EngineState.READY

    @pytest.mark.asyncio
    async def test_generate_image_success(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        api_response = _make_http_response(
            status=200,
            json_data={"image_url": "https://cdn.example.com/img.png"},
        )
        image_response = _make_http_response(read_data=b"\x89PNG\r\n\x1a\n")
        mock_session = _make_mock_session(
            post_responses=[api_response],
            get_responses=[image_response],
        )

        with patch("src.engine.image_engine.aiohttp.ClientSession", return_value=mock_session):
            image_data = await engine.generate_image("A red ball")

        assert image_data == b"\x89PNG\r\n\x1a\n"

    @pytest.mark.asyncio
    async def test_generate_success(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        api_response = _make_http_response(
            status=200,
            json_data={"image_url": "https://cdn.example.com/img.png"},
        )
        image_response = _make_http_response(read_data=b"\x89PNG\r\n\x1a\n")
        mock_session = _make_mock_session(
            post_responses=[api_response],
            get_responses=[image_response],
        )

        with patch("src.engine.image_engine.aiohttp.ClientSession", return_value=mock_session):
            request = GenerationRequest(prompt="A red ball")
            response = await engine.generate(request)

        assert response.text.startswith("data:image/png;base64,")
        assert response.provider == "nexa_api"
        assert response.finish_reason == "success"
        assert response.tokens_used > 0

    @pytest.mark.asyncio
    async def test_generate_http_401_raises_auth_error(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        mock_response = _make_http_response(
            status=401,
            json_data={"error": "Invalid API key"},
        )
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.image_engine.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(AuthenticationError, match="NexaAPI key"):
                await engine.generate_image("Test")

    @pytest.mark.asyncio
    async def test_generate_http_429_raises_rate_limit(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        mock_response = _make_http_response(status=429)
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.image_engine.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(RateLimitError, match="rate limit"):
                await engine.generate_image("Test")

    @pytest.mark.asyncio
    async def test_generate_http_400_raises_content_filter(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        mock_response = _make_http_response(
            status=400,
            text_data="Content policy violation",
        )
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.image_engine.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(ContentFilterError, match="Content filtered"):
                await engine.generate_image("Test")

    @pytest.mark.asyncio
    async def test_generate_generic_api_error(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        mock_response = _make_http_response(
            status=500,
            json_data={"error": "Internal server error"},
        )
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.image_engine.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(AIEngineError):
                await engine.generate_image("Test")

    @pytest.mark.asyncio
    async def test_api_key_not_leaked_in_errors(self) -> None:
        engine = self._make_engine(api_key="super-secret-nexa-key-12345")
        await engine.initialize()

        mock_response = _make_http_response(status=500, json_data={"error": "fail"})
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.image_engine.aiohttp.ClientSession", return_value=mock_session):
            try:
                await engine.generate_image("Test")
            except Exception as exc:
                assert "super-secret-nexa-key-12345" not in str(exc)


class TestSDXLEngine:
    """Tests for SDXLEngine (Replicate)."""

    def _make_engine(self, **overrides: Any) -> SDXLEngine:
        config = EngineConfig(
            provider="replicate",
            model="stability-ai/sdxl",
            api_key="test-replicate-key",
            timeout=5.0,
        )
        for k, v in overrides.items():
            setattr(config, k, v)
        return SDXLEngine(config=config)

    @pytest.mark.asyncio
    async def test_initialize_success(self) -> None:
        engine = self._make_engine()
        await engine.initialize()
        assert engine.state == EngineState.READY

    @pytest.mark.asyncio
    async def test_generate_image_success(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        create_response = _make_http_response(
            status=200,
            json_data={"urls": {"get": "https://api.replicate.com/preds/123"}},
        )
        poll_response = _make_http_response(
            status=200,
            json_data={
                "status": "succeeded",
                "output": [{"url": "https://cdn.example.com/sdxl.png"}],
            },
        )
        image_response = _make_http_response(read_data=b"\x89PNG\r\n\x1a\n")

        mock_session = _make_mock_session(
            post_responses=[create_response],
            get_responses=[poll_response, image_response],
        )

        with patch("src.engine.image_engine.aiohttp.ClientSession", return_value=mock_session):
            image_data = await engine.generate_image("A fantasy castle")

        assert image_data == b"\x89PNG\r\n\x1a\n"

    @pytest.mark.asyncio
    async def test_generate_http_401_raises_auth_error(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        mock_response = _make_http_response(status=401)
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.image_engine.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(AuthenticationError, match="Replicate"):
                await engine.generate_image("Test")

    @pytest.mark.asyncio
    async def test_generate_http_429_raises_rate_limit(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        mock_response = _make_http_response(status=429)
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.image_engine.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(RateLimitError, match="rate limit"):
                await engine.generate_image("Test")

    @pytest.mark.asyncio
    async def test_generate_poll_timeout(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        create_response = _make_http_response(
            status=200,
            json_data={"urls": {"get": "https://api.replicate.com/preds/123"}},
        )
        poll_response = _make_http_response(
            status=200,
            json_data={"status": "processing"},
        )
        mock_session = _make_mock_session(
            post_responses=[create_response],
            get_responses=[poll_response] * 30,
        )

        with patch("src.engine.image_engine.aiohttp.ClientSession", return_value=mock_session), \
             patch("src.engine.image_engine.asyncio.sleep", new_callable=AsyncMock):
            with pytest.raises(AIEngineError, match="timed out"):
                await engine.generate_image("Test")


class TestAgnesImageEngine:
    """Tests for AgnesImageEngine."""

    def _make_engine(self, **overrides: Any) -> AgnesImageEngine:
        config = EngineConfig(
            provider="agnes_ai",
            model="agnes-image",
            api_key="test-agnes-key",
            timeout=5.0,
        )
        for k, v in overrides.items():
            setattr(config, k, v)
        return AgnesImageEngine(config=config)

    @pytest.mark.asyncio
    async def test_initialize_success(self) -> None:
        engine = self._make_engine()
        await engine.initialize()
        assert engine.state == EngineState.READY

    @pytest.mark.asyncio
    async def test_generate_image_success(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        api_response = _make_http_response(
            status=200,
            json_data={"image_url": "https://cdn.example.com/agnes.png"},
        )
        image_response = _make_http_response(read_data=b"\x89PNG\r\n\x1a\n")
        mock_session = _make_mock_session(
            post_responses=[api_response],
            get_responses=[image_response],
        )

        with patch("src.engine.image_engine.aiohttp.ClientSession", return_value=mock_session):
            image_data = await engine.generate_image("A smiling sun")

        assert image_data == b"\x89PNG\r\n\x1a\n"

    @pytest.mark.asyncio
    async def test_generate_http_401_raises_auth_error(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        mock_response = _make_http_response(status=401)
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.image_engine.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(AuthenticationError, match="Agnes AI key"):
                await engine.generate_image("Test")

    @pytest.mark.asyncio
    async def test_generate_http_429_raises_rate_limit(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        mock_response = _make_http_response(status=429)
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.image_engine.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(RateLimitError, match="rate limit"):
                await engine.generate_image("Test")

    @pytest.mark.asyncio
    async def test_generate_no_image_url_raises_error(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        mock_response = _make_http_response(
            status=200,
            json_data={"unexpected": "response"},
        )
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.image_engine.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(AIEngineError, match="No image URL"):
                await engine.generate_image("Test")
