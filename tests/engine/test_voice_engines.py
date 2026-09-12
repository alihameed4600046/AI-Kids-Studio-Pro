"""Tests for voice generation engine implementations."""

from __future__ import annotations

import base64
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.engine.ai_engine import (
    AuthenticationError,
    EngineConfig,
    EngineState,
    GenerationRequest,
    AIEngineError,
    RateLimitError,
)
from src.engine.voice_engine import (
    AgnesVoiceEngine,
    AudioFormat,
    EdgeTTSEngine,
    GoogleTTSEngine,
    VoiceGender,
)


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


class TestEdgeTTSEngine:
    """Tests for EdgeTTSEngine (Microsoft Edge TTS)."""

    def _make_engine(self, **overrides: Any) -> EdgeTTSEngine:
        config = EngineConfig(
            provider="edge_tts",
            model="edge-tts",
            timeout=5.0,
        )
        for k, v in overrides.items():
            setattr(config, k, v)
        return EdgeTTSEngine(config=config)

    @pytest.mark.asyncio
    async def test_initialize_success(self) -> None:
        engine = self._make_engine()
        voices_response = _make_http_response(
            status=200,
            json_data=[{"ShortName": "en-US-AriaNeural", "Gender": "Female", "Locale": "en-US"}],
        )
        mock_session = _make_mock_session(get_responses=[voices_response])

        with patch("src.engine.voice_engine.aiohttp.ClientSession", return_value=mock_session):
            await engine.initialize()

        assert engine.state == EngineState.READY
        assert engine.is_ready

    @pytest.mark.asyncio
    async def test_initialize_handles_voice_fetch_failure(self) -> None:
        engine = self._make_engine()
        mock_session = _make_mock_session()

        with patch("src.engine.voice_engine.aiohttp.ClientSession", return_value=mock_session):
            await engine.initialize()

        assert engine.state == EngineState.READY

    @pytest.mark.asyncio
    async def test_generate_speech_success(self) -> None:
        engine = self._make_engine()
        voices_response = _make_http_response(
            status=200,
            json_data=[{"ShortName": "en-US-AriaNeural", "Gender": "Female", "Locale": "en-US"}],
        )
        audio_bytes = b"fake-mp3-audio-data"
        audio_response = _make_http_response(
            status=200,
            read_data=audio_bytes,
        )
        mock_session = _make_mock_session(get_responses=[voices_response, audio_response])

        with patch("src.engine.voice_engine.aiohttp.ClientSession", return_value=mock_session):
            await engine.initialize()
            audio_data = await engine.generate_speech("Hello world")

        assert audio_data == b"fake-mp3-audio-data"

    @pytest.mark.asyncio
    async def test_generate_success(self) -> None:
        engine = self._make_engine()
        voices_response = _make_http_response(
            status=200,
            json_data=[{"ShortName": "en-US-AriaNeural", "Gender": "Female", "Locale": "en-US"}],
        )
        audio_bytes = b"fake-mp3-audio-data"
        audio_response = _make_http_response(
            status=200,
            read_data=audio_bytes,
        )
        mock_session = _make_mock_session(get_responses=[voices_response, audio_response])

        with patch("src.engine.voice_engine.aiohttp.ClientSession", return_value=mock_session):
            await engine.initialize()
            request = GenerationRequest(prompt="Hello world")
            response = await engine.generate(request)

        assert response.text.startswith("data:audio/mp3;base64,")
        assert response.provider == "edge_tts"
        decoded = base64.b64decode(response.text.split(",", 1)[1])
        assert decoded == audio_bytes

    @pytest.mark.asyncio
    async def test_generate_speech_http_error(self) -> None:
        engine = self._make_engine()
        voices_response = _make_http_response(
            status=200,
            json_data=[{"ShortName": "en-US-AriaNeural", "Gender": "Female", "Locale": "en-US"}],
        )
        error_response = _make_http_response(status=500, text_data="Internal error")
        mock_session = _make_mock_session(get_responses=[voices_response, error_response])

        with patch("src.engine.voice_engine.aiohttp.ClientSession", return_value=mock_session):
            await engine.initialize()
            with pytest.raises(AIEngineError, match="Edge TTS failed"):
                await engine.generate_speech("Test")


class TestGoogleTTSEngine:
    """Tests for GoogleTTSEngine."""

    def _make_engine(self, **overrides: Any) -> GoogleTTSEngine:
        config = EngineConfig(
            provider="google_tts",
            model="google-tts",
            api_key="test-google-key",
            timeout=5.0,
        )
        for k, v in overrides.items():
            setattr(config, k, v)
        return GoogleTTSEngine(config=config)

    @pytest.mark.asyncio
    async def test_initialize_requires_api_key(self) -> None:
        engine = self._make_engine(api_key="")
        with pytest.raises(AIEngineError, match="API key"):
            await engine.initialize()

    @pytest.mark.asyncio
    async def test_initialize_success(self) -> None:
        engine = self._make_engine()
        await engine.initialize()
        assert engine.state == EngineState.READY

    @pytest.mark.asyncio
    async def test_generate_speech_success(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        b64_audio = base64.b64encode(b"fake-google-audio").decode("utf-8")
        mock_response = _make_http_response(
            status=200,
            json_data={"audioContent": b64_audio},
        )
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.voice_engine.aiohttp.ClientSession", return_value=mock_session):
            audio_data = await engine.generate_speech("Hello from Google")

        assert audio_data == b"fake-google-audio"

    @pytest.mark.asyncio
    async def test_generate_success(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        b64_audio = base64.b64encode(b"fake-google-audio").decode("utf-8")
        mock_response = _make_http_response(
            status=200,
            json_data={"audioContent": b64_audio},
        )
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.voice_engine.aiohttp.ClientSession", return_value=mock_session):
            request = GenerationRequest(prompt="Hello from Google")
            response = await engine.generate(request)

        assert response.text.startswith("data:audio/mp3;base64,")
        assert response.provider == "google_tts"

    @pytest.mark.asyncio
    async def test_generate_http_401_raises_auth_error(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        mock_response = _make_http_response(status=401)
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.voice_engine.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(AuthenticationError, match="Google TTS"):
                await engine.generate_speech("Test")

    @pytest.mark.asyncio
    async def test_generate_http_429_raises_rate_limit(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        mock_response = _make_http_response(status=429)
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.voice_engine.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(RateLimitError, match="rate limit"):
                await engine.generate_speech("Test")

    @pytest.mark.asyncio
    async def test_generate_no_audio_content_raises_error(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        mock_response = _make_http_response(
            status=200,
            json_data={"unexpected": "response"},
        )
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.voice_engine.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(AIEngineError, match="No audio content"):
                await engine.generate_speech("Test")


class TestAgnesVoiceEngine:
    """Tests for AgnesVoiceEngine."""

    def _make_engine(self, **overrides: Any) -> AgnesVoiceEngine:
        config = EngineConfig(
            provider="agnes_ai",
            model="agnes-voice",
            api_key="test-agnes-voice-key",
            timeout=5.0,
        )
        for k, v in overrides.items():
            setattr(config, k, v)
        return AgnesVoiceEngine(config=config)

    @pytest.mark.asyncio
    async def test_initialize_success(self) -> None:
        engine = self._make_engine()
        await engine.initialize()
        assert engine.state == EngineState.READY

    @pytest.mark.asyncio
    async def test_generate_speech_success(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        api_response = _make_http_response(
            status=200,
            json_data={"audio_url": "https://cdn.example.com/audio.mp3"},
        )
        audio_response = _make_http_response(read_data=b"fake-mp3-audio")
        mock_session = _make_mock_session(
            post_responses=[api_response],
            get_responses=[audio_response],
        )

        with patch("src.engine.voice_engine.aiohttp.ClientSession", return_value=mock_session):
            audio_data = await engine.generate_speech("Hello from Agnes")

        assert audio_data == b"fake-mp3-audio"

    @pytest.mark.asyncio
    async def test_generate_http_401_raises_auth_error(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        mock_response = _make_http_response(status=401)
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.voice_engine.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(AuthenticationError, match="Agnes AI key"):
                await engine.generate_speech("Test")

    @pytest.mark.asyncio
    async def test_generate_http_429_raises_rate_limit(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        mock_response = _make_http_response(status=429)
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.voice_engine.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(RateLimitError, match="rate limit"):
                await engine.generate_speech("Test")

    @pytest.mark.asyncio
    async def test_generate_no_audio_url_raises_error(self) -> None:
        engine = self._make_engine()
        await engine.initialize()

        mock_response = _make_http_response(
            status=200,
            json_data={"unexpected": "response"},
        )
        mock_session = _make_mock_session(post_responses=[mock_response])

        with patch("src.engine.voice_engine.aiohttp.ClientSession", return_value=mock_session):
            with pytest.raises(AIEngineError, match="No audio URL"):
                await engine.generate_speech("Test")
