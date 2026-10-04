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
    VoiceAccent,
    VoiceConfig,
    VoiceGender,
)


def _make_edge_voice(
    short_name: str = "en-US-AriaNeural",
    gender: str = "Female",
    locale: str = "en-US",
) -> dict[str, Any]:
    return {
        "Name": short_name,
        "ShortName": short_name,
        "Gender": gender,
        "Locale": locale,
        "FriendlyName": short_name,
    }


def _make_communicate_mock(chunks: list[dict[str, Any]] | None = None) -> MagicMock:
    """Build a mock edge_tts.Communicate yielding the given stream chunks."""
    _chunks = list(chunks if chunks is not None else [{"type": "audio", "data": b"fake-mp3-audio-data"}])

    async def _stream(*_args: Any, **_kwargs: Any):
        for chunk in _chunks:
            yield chunk

    communicate = MagicMock()
    communicate.stream = _stream
    return communicate


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
        mock_list_voices = AsyncMock(return_value=[_make_edge_voice()])

        with patch("src.engine.voice_engine.edge_tts.list_voices", mock_list_voices):
            await engine.initialize()

        assert engine.state == EngineState.READY
        assert engine.is_ready

    @pytest.mark.asyncio
    async def test_initialize_uses_edge_tts_list_voices(self) -> None:
        engine = self._make_engine()
        mock_list_voices = AsyncMock(return_value=[_make_edge_voice()])

        with patch("src.engine.voice_engine.edge_tts.list_voices", mock_list_voices):
            await engine.initialize()

        mock_list_voices.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_fetch_voices_maps_voice_fields(self) -> None:
        engine = self._make_engine()
        mock_list_voices = AsyncMock(
            return_value=[
                {
                    "Name": "Microsoft Aria Online (Natural) - English (United States)",
                    "ShortName": "en-US-AriaNeural",
                    "Gender": "Female",
                    "Locale": "en-US",
                    "SuggestedCodec": "audio-24khz-48kbitrate-mono-mp3",
                    "FriendlyName": "Aria",
                    "Status": "Active",
                    "VoiceTag": {"VoicePersonalities": []},
                }
            ]
        )

        with patch("src.engine.voice_engine.edge_tts.list_voices", mock_list_voices):
            await engine.initialize()

        assert len(engine.get_available_voices()) == 1
        voice = engine.get_available_voices()[0]
        assert voice["ShortName"] == "en-US-AriaNeural"
        assert voice["Gender"] == "Female"
        assert voice["Locale"] == "en-US"

    @pytest.mark.asyncio
    async def test_initialize_handles_voice_fetch_failure(self) -> None:
        engine = self._make_engine()
        mock_list_voices = AsyncMock(side_effect=RuntimeError("network down"))

        with patch("src.engine.voice_engine.edge_tts.list_voices", mock_list_voices):
            await engine.initialize()

        assert engine.state == EngineState.READY
        assert engine.get_available_voices() == []

    @pytest.mark.asyncio
    async def test_generate_speech_success(self) -> None:
        engine = self._make_engine()
        mock_list_voices = AsyncMock(return_value=[_make_edge_voice()])
        communicate = _make_communicate_mock()

        with (
            patch("src.engine.voice_engine.edge_tts.list_voices", mock_list_voices),
            patch("src.engine.voice_engine.edge_tts.Communicate", return_value=communicate) as mock_communicate,
        ):
            await engine.initialize()
            audio_data = await engine.generate_speech("Hello world")

        assert audio_data == b"fake-mp3-audio-data"
        assert mock_communicate.call_args.args[0] == "Hello world"

    @pytest.mark.asyncio
    async def test_generate_speech_passes_selected_voice(self) -> None:
        engine = self._make_engine()
        mock_list_voices = AsyncMock(
            return_value=[
                _make_edge_voice(short_name="en-US-AriaNeural", gender="Female", locale="en-US"),
                _make_edge_voice(short_name="en-US-JennyNeural", gender="Female", locale="en-US"),
            ]
        )
        communicate = _make_communicate_mock()
        config = VoiceConfig()

        with (
            patch("src.engine.voice_engine.edge_tts.list_voices", mock_list_voices),
            patch("src.engine.voice_engine.edge_tts.Communicate", return_value=communicate) as mock_communicate,
        ):
            await engine.initialize()
            expected_voice = engine._select_default_voice(config)
            await engine.generate_speech("Test", config)

        assert mock_communicate.call_args.args[1] == expected_voice

    def test_select_default_voice_matches_gender_and_locale(self) -> None:
        engine = self._make_engine()
        engine._voices = [
            _make_edge_voice(short_name="en-GB-RyanNeural", gender="Male", locale="british"),
            _make_edge_voice(short_name="en-US-AriaNeural", gender="Female", locale="american"),
        ]

        config = VoiceConfig(gender=VoiceGender.MALE, accent=VoiceAccent.BRITISH)

        assert engine._select_default_voice(config) == "en-GB-RyanNeural"

    def test_select_default_voice_falls_back_to_aria(self) -> None:
        engine = self._make_engine()
        engine._voices = []

        assert engine._select_default_voice(VoiceConfig()) == "en-US-AriaNeural"

    @pytest.mark.asyncio
    async def test_generate_speech_uses_explicit_voice_id(self) -> None:
        engine = self._make_engine()
        mock_list_voices = AsyncMock(return_value=[_make_edge_voice()])
        communicate = _make_communicate_mock()

        with (
            patch("src.engine.voice_engine.edge_tts.list_voices", mock_list_voices),
            patch("src.engine.voice_engine.edge_tts.Communicate", return_value=communicate) as mock_communicate,
        ):
            await engine.initialize()
            await engine.generate_speech("Test", VoiceConfig(voice_id="en-US-JennyNeural"))

        assert mock_communicate.call_args.args[1] == "en-US-JennyNeural"

    @pytest.mark.asyncio
    async def test_generate_speech_maps_rate_pitch_volume(self) -> None:
        engine = self._make_engine()
        mock_list_voices = AsyncMock(return_value=[_make_edge_voice()])
        communicate = _make_communicate_mock()

        with (
            patch("src.engine.voice_engine.edge_tts.list_voices", mock_list_voices),
            patch("src.engine.voice_engine.edge_tts.Communicate", return_value=communicate) as mock_communicate,
        ):
            await engine.initialize()
            await engine.generate_speech(
                "Test",
                VoiceConfig(speed=1.5, pitch=-3.0, volume=0.5),
            )

        kwargs = mock_communicate.call_args.kwargs
        assert kwargs["rate"] == "+50%"
        assert kwargs["pitch"] == "-3Hz"
        assert kwargs["volume"] == "-50%"

    @pytest.mark.asyncio
    async def test_generate_speech_default_rate_pitch_volume(self) -> None:
        engine = self._make_engine()
        mock_list_voices = AsyncMock(return_value=[_make_edge_voice()])
        communicate = _make_communicate_mock()

        with (
            patch("src.engine.voice_engine.edge_tts.list_voices", mock_list_voices),
            patch("src.engine.voice_engine.edge_tts.Communicate", return_value=communicate) as mock_communicate,
        ):
            await engine.initialize()
            await engine.generate_speech("Test")

        kwargs = mock_communicate.call_args.kwargs
        assert kwargs["rate"] == "+0%"
        assert kwargs["pitch"] == "+0Hz"
        assert kwargs["volume"] == "+0%"

    @pytest.mark.asyncio
    async def test_generate_speech_collects_multiple_chunks(self) -> None:
        engine = self._make_engine()
        mock_list_voices = AsyncMock(return_value=[_make_edge_voice()])
        communicate = _make_communicate_mock(
            chunks=[
                {"type": "audio", "data": b"chunk-one"},
                {"type": "WordBoundary", "text": "hello"},
                {"type": "audio", "data": b"chunk-two"},
            ]
        )

        with (
            patch("src.engine.voice_engine.edge_tts.list_voices", mock_list_voices),
            patch("src.engine.voice_engine.edge_tts.Communicate", return_value=communicate),
        ):
            await engine.initialize()
            audio_data = await engine.generate_speech("Test")

        assert audio_data == b"chunk-onechunk-two"

    @pytest.mark.asyncio
    async def test_generate_success(self) -> None:
        engine = self._make_engine()
        mock_list_voices = AsyncMock(return_value=[_make_edge_voice()])
        audio_bytes = b"fake-mp3-audio-data"
        communicate = _make_communicate_mock(chunks=[{"type": "audio", "data": audio_bytes}])

        with (
            patch("src.engine.voice_engine.edge_tts.list_voices", mock_list_voices),
            patch("src.engine.voice_engine.edge_tts.Communicate", return_value=communicate),
        ):
            await engine.initialize()
            request = GenerationRequest(prompt="Hello world")
            response = await engine.generate(request)

        assert response.text.startswith("data:audio/mp3;base64,")
        assert response.provider == "edge_tts"
        decoded = base64.b64decode(response.text.split(",", 1)[1])
        assert decoded == audio_bytes

    @pytest.mark.asyncio
    async def test_generate_speech_stream_error_raises(self) -> None:
        engine = self._make_engine()
        mock_list_voices = AsyncMock(return_value=[_make_edge_voice()])

        async def _failing_stream(*_args: Any, **_kwargs: Any):
            raise RuntimeError("websocket closed")
            yield  # pragma: no cover

        communicate = MagicMock()
        communicate.stream = _failing_stream

        with (
            patch("src.engine.voice_engine.edge_tts.list_voices", mock_list_voices),
            patch("src.engine.voice_engine.edge_tts.Communicate", return_value=communicate),
        ):
            await engine.initialize()
            with pytest.raises(AIEngineError, match="Edge TTS generation failed"):
                await engine.generate_speech("Test")

        assert engine.state == EngineState.ERROR

    @pytest.mark.asyncio
    async def test_generate_speech_empty_audio_raises(self) -> None:
        engine = self._make_engine()
        mock_list_voices = AsyncMock(return_value=[_make_edge_voice()])
        communicate = _make_communicate_mock(chunks=[{"type": "WordBoundary", "text": "hi"}])

        with (
            patch("src.engine.voice_engine.edge_tts.list_voices", mock_list_voices),
            patch("src.engine.voice_engine.edge_tts.Communicate", return_value=communicate),
        ):
            await engine.initialize()
            with pytest.raises(AIEngineError, match="no audio data"):
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
