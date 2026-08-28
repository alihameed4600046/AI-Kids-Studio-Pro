"""Voice generation engines for AI Kids Studio Pro.

This module provides text-to-speech engines including Edge TTS,
Google TTS, and Agnes AI voice generation.
"""

from __future__ import annotations

import asyncio
import base64
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Sequence

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


class VoiceGender(Enum):
    """Voice gender options."""

    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"
    BOY = "boy"
    GIRL = "girl"


class VoiceAccent(Enum):
    """Voice accent options."""

    AMERICAN = "american"
    BRITISH = "british"
    AUSTRALIAN = "australian"
    SPANISH = "spanish"
    FRENCH = "french"
    GERMAN = "german"
    INDIAN = "indian"
    JAPANESE = "japanese"


class AudioFormat(Enum):
    """Supported audio formats."""

    MP3 = "mp3"
    WAV = "wav"
    OGG = "ogg"
    AAC = "aac"


@dataclass
class VoiceConfig:
    """Configuration for voice generation."""

    voice_id: str = "default"
    gender: VoiceGender = VoiceGender.NEUTRAL
    accent: VoiceAccent = VoiceAccent.AMERICAN
    speed: float = 1.0
    pitch: float = 0.0
    volume: float = 1.0
    format: AudioFormat = AudioFormat.MP3
    output_path: Path | None = None

    def __post_init__(self) -> None:
        if self.speed < 0.5 or self.speed > 2.0:
            raise ValueError("Speed must be between 0.5 and 2.0")
        if self.pitch < -12 or self.pitch > 12:
            raise ValueError("Pitch must be between -12 and 12 semitones")
        if self.volume < 0.0 or self.volume > 1.0:
            raise ValueError("Volume must be between 0.0 and 1.0")


class VoiceEngine(AIEngine, ABC):
    """Abstract base class for voice generation engines."""

    def __init__(self, config: EngineConfig | None = None) -> None:
        super().__init__(config)
        self.voice_config = VoiceConfig()

    @abstractmethod
    async def generate_speech(
        self,
        text: str,
        config: VoiceConfig | None = None,
    ) -> bytes:
        """Generate speech from text.

        Parameters
        ----------
        text:
            Text to convert to speech.
        config:
            Voice generation configuration.

        Returns
        -------
        bytes
            Generated audio data.
        """
        if self._state != EngineState.READY:
            raise EngineNotReadyError(
                f"Voice engine {self.__class__.__name__} is not ready",
                provider=self._config.provider,
            )

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        """Generate speech from a GenerationRequest.

        Parameters
        ----------
        request:
            Generation request with text and metadata.

        Returns
        -------
        GenerationResponse
            Response with audio data as base64-encoded string.
        """
        if self._state != EngineState.READY:
            raise EngineNotReadyError(
                f"Voice engine {self.__class__.__name__} is not ready",
                provider=self._config.provider,
            )

        self._state = EngineState.GENERATING
        start_time = time.time()

        try:
            audio_data = await self.generate_speech(
                request.prompt,
                request.metadata.get("voice_config"),
            )
            latency = (time.time() - start_time) * 1000

            audio_b64 = base64.b64encode(audio_data).decode("utf-8")
            self._record_success()
            self._state = EngineState.READY

            return GenerationResponse(
                text=f"data:audio/mp3;base64,{audio_b64}",
                model=request.model or self._config.model,
                provider=self._config.provider,
                tokens_used=len(request.prompt.split()),
                finish_reason="success",
                latency_ms=latency,
                metadata={"audio_format": AudioFormat.MP3.value, "size": len(audio_data)},
            )
        except Exception as exc:
            self._record_error(exc)
            self._state = EngineState.ERROR
            raise AIEngineError(
                f"Voice generation failed: {exc}", provider=self._config.provider
            ) from exc

    async def stream(self, request: GenerationRequest):
        """Voice engines don't support streaming."""
        raise NotImplementedError("Voice generation does not support streaming")

    async def validate(self) -> bool:
        """Validate voice engine connectivity."""
        return self._state == EngineState.READY


class EdgeTTSEngine(VoiceEngine):
    """Microsoft Edge TTS engine.

    Edge TTS is a free text-to-speech service with high-quality voices.
    No API key required.
    """

    def __init__(self, config: EngineConfig | None = None) -> None:
        if config is None:
            config = EngineConfig(
                provider="edge_tts",
                model="edge-tts",
                timeout=30.0,
            )
        super().__init__(config)
        self.base_url = "https://dictate.microsoft.com/api/speech"
        self._voices: list[dict[str, Any]] = []

    async def initialize(self) -> None:
        """Initialize the Edge TTS engine."""
        self._state = EngineState.LOADING
        try:
            await self._fetch_voices()
            self._state = EngineState.READY
            logger.info("Edge TTS engine initialized with %d voices", len(self._voices))
        except Exception as exc:
            self._state = EngineState.ERROR
            logger.error("Failed to initialize Edge TTS: %s", exc)
            raise

    async def _fetch_voices(self) -> None:
        """Fetch available voices from Edge TTS."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://dictate.microsoft.com/api/speech/voices"
                ) as response:
                    if response.status == 200:
                        self._voices = await response.json()
                    else:
                        logger.warning("Could not fetch Edge TTS voices")
                        self._voices = []
        except Exception as exc:
            logger.warning("Error fetching voices: %s", exc)
            self._voices = []

    async def generate_speech(
        self,
        text: str,
        config: VoiceConfig | None = None,
    ) -> bytes:
        """Generate speech using Edge TTS.

        Parameters
        ----------
        text:
            Text to convert to speech.
        config:
            Voice configuration.

        Returns
        -------
        bytes
            Generated audio data.
        """
        config = config or self.voice_config
        self._state = EngineState.GENERATING

        voice_name = config.voice_id
        if not voice_name or voice_name == "default":
            voice_name = self._select_default_voice(config)

        url = f"{self.base_url}/synthesize"
        params = {
            "text": text,
            "voice": voice_name,
            "speed": str(config.speed),
            "pitch": str(config.pitch),
            "format": config.format.value,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url, params=params, timeout=self._config.timeout
                ) as response:
                    if response.status == 200:
                        audio_data = await response.read()
                        self._record_success()
                        self._state = EngineState.READY
                        return audio_data
                    else:
                        error_text = await response.text()
                        raise AIEngineError(
                            f"Edge TTS failed ({response.status}): {error_text}",
                            provider=self._config.provider,
                        )
        except AIEngineError:
            raise
        except Exception as exc:
            self._state = EngineState.ERROR
            raise AIEngineError(
                f"Edge TTS generation failed: {exc}", provider=self._config.provider
            ) from exc

    def _select_default_voice(self, config: VoiceConfig) -> str:
        """Select a default voice based on configuration."""
        gender = config.gender.value
        accent = config.accent.value

        for voice in self._voices:
            voice_gender = voice.get("Gender", "").lower()
            voice_locale = voice.get("Locale", "").lower()
            if gender in voice_gender and accent in voice_locale:
                return voice.get("ShortName", "en-US-AriaNeural")

        return "en-US-AriaNeural"

    def get_available_voices(self) -> list[dict[str, Any]]:
        """Get list of available voices.

        Returns
        -------
        list[dict[str, Any]]
            List of voice information dictionaries.
        """
        return self._voices


class GoogleTTSEngine(VoiceEngine):
    """Google Cloud Text-to-Speech engine.

    Requires Google Cloud credentials.
    """

    def __init__(self, config: EngineConfig | None = None) -> None:
        if config is None:
            config = EngineConfig(
                provider="google_tts",
                model="google-tts",
                api_key=None,
                timeout=30.0,
            )
        super().__init__(config)
        self.base_url = "https://texttospeech.googleapis.com/v1"

    async def initialize(self) -> None:
        """Initialize the Google TTS engine."""
        self._state = EngineState.LOADING
        if not self._config.api_key:
            raise AIEngineError(
                "Google TTS requires an API key", provider=self._config.provider
            )
        self._state = EngineState.READY
        logger.info("Google TTS engine initialized")

    async def generate_speech(
        self,
        text: str,
        config: VoiceConfig | None = None,
    ) -> bytes:
        """Generate speech using Google TTS.

        Parameters
        ----------
        text:
            Text to convert to speech.
        config:
            Voice configuration.

        Returns
        -------
        bytes
            Generated audio data.
        """
        config = config or self.voice_config
        self._state = EngineState.GENERATING

        headers = {
            "Authorization": f"Bearer {self._config.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "input": {"text": text},
            "voice": {
                "languageCode": "en-US",
                "name": config.voice_id,
                "ssmlGender": config.gender.value.upper(),
            },
            "audioConfig": {
                "audioEncoding": config.format.value.upper(),
                "speakingRate": config.speed,
                "pitch": config.pitch,
                "volumeGainDb": 20 * config.volume,
            },
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/text:synthesize",
                    json=payload,
                    headers=headers,
                    timeout=self._config.timeout,
                ) as response:
                    if response.status == 401:
                        raise AuthenticationError(
                            "Invalid Google TTS credentials",
                            provider=self._config.provider,
                        )
                    if response.status == 429:
                        raise RateLimitError(
                            "Google TTS rate limit exceeded",
                            provider=self._config.provider,
                        )

                    result = await response.json()
                    audio_content = result.get("audioContent")
                    if not audio_content:
                        raise AIEngineError(
                            "No audio content in response",
                            provider=self._config.provider,
                        )

                    audio_data = base64.b64decode(audio_content)
                    self._record_success()
                    self._state = EngineState.READY
                    return audio_data
        except AIEngineError:
            raise
        except Exception as exc:
            self._state = EngineState.ERROR
            raise AIEngineError(
                f"Google TTS generation failed: {exc}",
                provider=self._config.provider,
            ) from exc


class AgnesVoiceEngine(VoiceEngine):
    """Agnes AI voice generation engine.

    Agnes AI provides free text-to-speech generation.
    """

    def __init__(self, config: EngineConfig | None = None) -> None:
        if config is None:
            config = EngineConfig(
                provider="agnes_ai",
                model="agnes-voice",
                api_key=None,
                timeout=30.0,
            )
        super().__init__(config)
        self.base_url = "https://api.agnes-ai.com/v1"

    async def initialize(self) -> None:
        """Initialize the Agnes voice engine."""
        self._state = EngineState.LOADING
        if not self._config.api_key:
            logger.warning("No API key provided for Agnes AI")
        self._state = EngineState.READY
        logger.info("Agnes voice engine initialized")

    async def generate_speech(
        self,
        text: str,
        config: VoiceConfig | None = None,
    ) -> bytes:
        """Generate speech using Agnes AI.

        Parameters
        ----------
        text:
            Text to convert to speech.
        config:
            Voice configuration.

        Returns
        -------
        bytes
            Generated audio data.
        """
        config = config or self.voice_config
        self._state = EngineState.GENERATING

        headers = {
            "Authorization": f"Bearer {self._config.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "text": text,
            "voice_id": config.voice_id,
            "gender": config.gender.value,
            "accent": config.accent.value,
            "speed": config.speed,
            "pitch": config.pitch,
            "format": config.format.value,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/tts/generate",
                    json=payload,
                    headers=headers,
                    timeout=self._config.timeout,
                ) as response:
                    if response.status == 401:
                        raise AuthenticationError(
                            "Invalid Agnes AI key", provider=self._config.provider
                        )
                    if response.status == 429:
                        raise RateLimitError(
                            "Agnes AI rate limit exceeded",
                            provider=self._config.provider,
                        )

                    result = await response.json()
                    audio_url = result.get("audio_url") or result.get("url")

                    if not audio_url:
                        raise AIEngineError(
                            "No audio URL in response",
                            provider=self._config.provider,
                        )

                    async with session.get(audio_url) as audio_response:
                        audio_data = await audio_response.read()

                    self._record_success()
                    self._state = EngineState.READY
                    return audio_data
        except AIEngineError:
            raise
        except Exception as exc:
            self._state = EngineState.ERROR
            raise AIEngineError(
                f"Agnes voice generation failed: {exc}",
                provider=self._config.provider,
            ) from exc
