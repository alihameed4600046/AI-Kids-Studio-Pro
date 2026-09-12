"""Tests for video generation engine implementations."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.engine.ai_engine import (
    AIEngineError,
    AuthenticationError,
    EngineConfig,
    EngineState,
    GenerationRequest,
    GenerationResponse,
    RateLimitError,
)
from src.engine.video_engine import AgnesVideoEngine, MockVideoEngine


def _make_http_response(
    status: int = 200,
    json_data: dict[str, Any] | None = None,
    text_data: str | None = None,
    read_data: bytes = b"",
) -> MagicMock:
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


class TestAgnesVideoEngine:
    """Tests for AgnesVideoEngine."""

    def _make_engine(self, **overrides: Any) -> AgnesVideoEngine:
        config = EngineConfig(
            provider="agnes_ai",
            model="agnes-video",
            api_key="test-agnes-video-key",
            timeout=5.0,
        )
        for k, v in overrides.items():
            setattr(config, k, v)
        return AgnesVideoEngine(config=config)

    @pytest.mark.asyncio
    async def test_initialize_success(self) -> None:
        engine = self._make_engine()
        await engine.initialize()
        assert engine.state == EngineState.READY
        assert engine.is_ready

    @pytest.mark.asyncio
    async def test_generate_video_success(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        api_response = _make_http_response(
            status=200,
            json_data={"video_url": "https://cdn.example.com/video.mp4"},
        )
        video_response = _make_http_response(read_data=b"\x00\x00\x00\x20ftyp")
        mock_session = _make_mock_session(
            post_responses=[api_response],
            get_responses=[video_response],
        )

        with patch("src.engine.video_engine.aiohttp.ClientSession", return_value=mock_session):
            video_data = await engine.generate_video("A dancing robot")

        assert video_data == b"\x00\x00\x00\x20ftyp"

    @pytest.mark.asyncio
    async def test_generate_success(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        api_response = _make_http_response(
            status=200,
            json_data={"video_url": "https://cdn.example.com/video.mp4"},
        )
        video_response = _make_http_response(read_data=b"\x00\x00\x00\x20ftyp")
        mock_session = _make_mock_session(
            post_responses=[api_response],
            get_responses=[video_response],
        )

        with patch("src.engine.video_engine.aiohttp.ClientSession", return_value=mock_session):
            request = GenerationRequest(prompt="A dancing robot")
            response = await engine.generate(request)

        assert response.text.startswith("data:video/mp4;base64,")
        assert response.provider == "agnes_ai"
        assert response.finish_reason == "success"

    @pytest.mark.asyncio
    async def test_generate_http_401_raises_auth_error(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        mock_response = _make_http_response(status=401)
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.video_engine.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(AuthenticationError, match="Agnes AI key"):
                await engine.generate_video("Test")

    @pytest.mark.asyncio
    async def test_generate_http_429_raises_rate_limit(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        mock_response = _make_http_response(status=429)
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.video_engine.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(RateLimitError, match="rate limit"):
                await engine.generate_video("Test")

    @pytest.mark.asyncio
    async def test_generate_http_400_raises_content_filter(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        from src.engine.ai_engine import ContentFilterError

        mock_response = _make_http_response(
            status=400,
            text_data="Content filtered",
        )
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.video_engine.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(ContentFilterError):
                await engine.generate_video("Test")

    @pytest.mark.asyncio
    async def test_generate_no_video_url_raises_error(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        mock_response = _make_http_response(
            status=200,
            json_data={"unexpected": "response"},
        )
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.video_engine.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(AIEngineError, match="No video URL"):
                await engine.generate_video("Test")


class TestMockVideoEngine:
    """Tests for MockVideoEngine."""

    def _make_engine(self, **overrides: Any) -> MockVideoEngine:
        config = EngineConfig(
            provider="mock",
            model="mock-video",
            timeout=5.0,
        )
        for k, v in overrides.items():
            setattr(config, k, v)
        return MockVideoEngine(config=config)

    @pytest.mark.asyncio
    async def test_initialize_success(self) -> None:
        engine = self._make_engine()
        await engine.initialize()
        assert engine.state == EngineState.READY
        assert engine.is_ready

    @pytest.mark.asyncio
    async def test_generate_video_returns_deterministic_data(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        video_data = await engine.generate_video("Any prompt")
        assert video_data == b"MOCK_VIDEO_DATA"

    @pytest.mark.asyncio
    async def test_generate_returns_deterministic_response(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        request = GenerationRequest(prompt="Test prompt")
        response = await engine.generate(request)

        assert isinstance(response, GenerationResponse)
        assert response.text == "[Mock video generated]"
        assert response.provider == "mock"
        assert response.model == "mock-video"
        assert response.finish_reason == "success"
        assert response.tokens_used == 2
        assert response.metadata["mock"] is True

    @pytest.mark.asyncio
    async def test_generate_video_call_count(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        for _ in range(3):
            data = await engine.generate_video("Test")
            assert data == b"MOCK_VIDEO_DATA"
