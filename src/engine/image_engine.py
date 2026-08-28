"""Image generation engines for AI Kids Studio Pro.

This module provides image generation engines including Flux (NexaAPI),
SDXL (Replicate), and Agnes AI image generation.
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
    ContentFilterError,
    EngineConfig,
    EngineState,
    GenerationRequest,
    GenerationResponse,
)
from src.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


class ImageFormat(Enum):
    """Supported image formats."""

    PNG = "png"
    JPEG = "jpeg"
    WEBP = "webp"


class ImageStyle(Enum):
    """Supported image styles."""

    REALISTIC = "realistic"
    CARTOON = "cartoon"
    ANIME = "anime"
    PIXEL_ART = "pixel_art"
    WATERCOLOR = "watercolor"
    OIL_PAINTING = "oil_painting"
    CLAYMATION = "claymation"
    SKETCH = "sketch"


@dataclass
class ImageConfig:
    """Configuration for image generation."""

    width: int = 1024
    height: int = 1024
    steps: int = 30
    guidance_scale: float = 7.5
    seed: int | None = None
    style: ImageStyle | None = None
    format: ImageFormat = ImageFormat.PNG
    negative_prompt: str | None = None

    def __post_init__(self) -> None:
        if self.width < 256 or self.height < 256:
            raise ValueError("Image dimensions must be at least 256x256")
        if self.steps < 1 or self.steps > 150:
            raise ValueError("Steps must be between 1 and 150")
        if self.guidance_scale < 0 or self.guidance_scale > 30:
            raise ValueError("Guidance scale must be between 0 and 30")


class ImageEngine(AIEngine, ABC):
    """Abstract base class for image generation engines."""

    def __init__(self, config: EngineConfig | None = None) -> None:
        super().__init__(config)
        self.image_config = ImageConfig()

    @abstractmethod
    async def generate_image(
        self,
        prompt: str,
        config: ImageConfig | None = None,
    ) -> bytes:
        """Generate an image from a text prompt.

        Parameters
        ----------
        prompt:
            Text description of the image to generate.
        config:
            Image generation configuration.

        Returns
        -------
        bytes
            Generated image data.
        """
        if self._state != EngineState.READY:
            raise EngineNotReadyError(
                f"Image engine {self.__class__.__name__} is not ready",
                provider=self._config.provider,
            )

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        """Generate an image from a GenerationRequest.

        Parameters
        ----------
        request:
            Generation request with prompt and metadata.

        Returns
        -------
        GenerationResponse
            Response with image data as base64-encoded string.
        """
        if self._state != EngineState.READY:
            raise EngineNotReadyError(
                f"Image engine {self.__class__.__name__} is not ready",
                provider=self._config.provider,
            )

        self._state = EngineState.GENERATING
        start_time = time.time()

        try:
            image_data = await self.generate_image(
                request.prompt,
                request.metadata.get("image_config"),
            )
            latency = (time.time() - start_time) * 1000

            image_b64 = base64.b64encode(image_data).decode("utf-8")
            self._record_success()
            self._state = EngineState.READY

            return GenerationResponse(
                text=f"data:image/png;base64,{image_b64}",
                model=request.model or self._config.model,
                provider=self._config.provider,
                tokens_used=len(request.prompt.split()),
                finish_reason="success",
                latency_ms=latency,
                metadata={"image_format": ImageFormat.PNG.value, "size": len(image_data)},
            )
        except Exception as exc:
            self._record_error(exc)
            self._state = EngineState.ERROR
            raise AIEngineError(
                f"Image generation failed: {exc}", provider=self._config.provider
            ) from exc

    async def stream(self, request: GenerationRequest):
        """Image engines don't support streaming."""
        raise NotImplementedError("Image generation does not support streaming")

    async def validate(self) -> bool:
        """Validate image engine connectivity."""
        return self._state == EngineState.READY

    def _estimate_tokens(self, prompt: str) -> int:
        """Estimate token count for a prompt."""
        return len(prompt.split())


class FluxEngine(ImageEngine):
    """Flux image generation engine using NexaAPI.

    NexaAPI provides Flux models for high-quality image generation.
    Pricing: ~$0.001 per image.
    """

    def __init__(self, config: EngineConfig | None = None) -> None:
        if config is None:
            config = EngineConfig(
                provider="nexa_api",
                model="flux-schnell",
                api_key=None,
                timeout=60.0,
            )
        super().__init__(config)
        self.base_url = "https://api.nexaapi.com/v1"

    async def initialize(self) -> None:
        """Initialize the Flux engine."""
        self._state = EngineState.LOADING
        if not self._config.api_key:
            logger.warning("No API key provided for NexaAPI")
        self._state = EngineState.READY
        logger.info("Flux engine initialized")

    async def generate_image(
        self,
        prompt: str,
        config: ImageConfig | None = None,
    ) -> bytes:
        """Generate image using Flux via NexaAPI.

        Parameters
        ----------
        prompt:
            Text description of the image.
        config:
            Image generation configuration.

        Returns
        -------
        bytes
            Generated image data.
        """
        config = config or self.image_config
        self._state = EngineState.GENERATING

        headers = {
            "Authorization": f"Bearer {self._config.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "prompt": prompt,
            "width": config.width,
            "height": config.height,
            "steps": config.steps,
            "guidance_scale": config.guidance_scale,
            "output_format": config.format.value,
        }
        if config.seed is not None:
            payload["seed"] = config.seed
        if config.negative_prompt:
            payload["negative_prompt"] = config.negative_prompt

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/images/generate",
                    json=payload,
                    headers=headers,
                    timeout=self._config.timeout,
                ) as response:
                    if response.status == 401:
                        raise AuthenticationError(
                            "Invalid NexaAPI key", provider=self._config.provider
                        )
                    if response.status == 429:
                        raise RateLimitError(
                            "NexaAPI rate limit exceeded",
                            provider=self._config.provider,
                        )
                    if response.status == 400:
                        error_text = await response.text()
                        raise ContentFilterError(
                            f"Content filtered: {error_text}",
                            provider=self._config.provider,
                        )

                    result = await response.json()
                    image_url = result.get("image_url") or result.get("url")

                    if not image_url:
                        raise AIEngineError(
                            "No image URL in response", provider=self._config.provider
                        )

                    async with session.get(image_url) as img_response:
                        image_data = await img_response.read()

                    self._record_success()
                    self._state = EngineState.READY
                    return image_data
        except AIEngineError:
            raise
        except Exception as exc:
            self._state = EngineState.ERROR
            raise AIEngineError(
                f"Flux generation failed: {exc}", provider=self._config.provider
            ) from exc


class SDXLEngine(ImageEngine):
    """SDXL image generation engine using Replicate.

    Replicate provides SDXL models for image generation.
    """

    def __init__(self, config: EngineConfig | None = None) -> None:
        if config is None:
            config = EngineConfig(
                provider="replicate",
                model="stability-ai/sdxl",
                api_key=None,
                timeout=120.0,
            )
        super().__init__(config)
        self.base_url = "https://api.replicate.com/v1"

    async def initialize(self) -> None:
        """Initialize the SDXL engine."""
        self._state = EngineState.LOADING
        if not self._config.api_key:
            logger.warning("No API key provided for Replicate")
        self._state = EngineState.READY
        logger.info("SDXL engine initialized")

    async def generate_image(
        self,
        prompt: str,
        config: ImageConfig | None = None,
    ) -> bytes:
        """Generate image using SDXL via Replicate.

        Parameters
        ----------
        prompt:
            Text description of the image.
        config:
            Image generation configuration.

        Returns
        -------
        bytes
            Generated image data.
        """
        config = config or self.image_config
        self._state = EngineState.GENERATING

        headers = {
            "Authorization": f"Token {self._config.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "version": "39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            "input": {
                "prompt": prompt,
                "width": config.width,
                "height": config.height,
                "num_inference_steps": config.steps,
                "guidance_scale": config.guidance_scale,
                "output_format": config.format.value,
            },
        }
        if config.seed is not None:
            payload["input"]["seed"] = config.seed
        if config.negative_prompt:
            payload["input"]["negative_prompt"] = config.negative_prompt

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/predictions",
                    json=payload,
                    headers=headers,
                    timeout=self._config.timeout,
                ) as response:
                    if response.status in (401, 403):
                        raise AuthenticationError(
                            "Invalid Replicate API key",
                            provider=self._config.provider,
                        )
                    if response.status == 429:
                        raise RateLimitError(
                            "Replicate rate limit exceeded",
                            provider=self._config.provider,
                        )

                    result = await response.json()
                    prediction_url = result.get("urls", {}).get("get")

                    if not prediction_url:
                        raise AIEngineError(
                            "No prediction URL in response",
                            provider=self._config.provider,
                        )

                    for _ in range(30):
                        async with session.get(
                            prediction_url, headers=headers
                        ) as poll_response:
                            poll_result = await poll_response.json()
                            if poll_result.get("status") == "succeeded":
                                image_url = poll_result.get("output", [{}])[0]
                                if isinstance(image_url, dict):
                                    image_url = image_url.get("url")
                                async with session.get(image_url) as img_response:
                                    image_data = await img_response.read()
                                self._record_success()
                                self._state = EngineState.READY
                                return image_data
                            elif poll_result.get("status") == "failed":
                                raise AIEngineError(
                                    "Replicate prediction failed",
                                    provider=self._config.provider,
                                )
                        await asyncio.sleep(1)

                    raise AIEngineError(
                        "Replicate prediction timed out",
                        provider=self._config.provider,
                    )
        except AIEngineError:
            raise
        except Exception as exc:
            self._state = EngineState.ERROR
            raise AIEngineError(
                f"SDXL generation failed: {exc}", provider=self._config.provider
            ) from exc


class AgnesImageEngine(ImageEngine):
    """Agnes AI image generation engine.

    Agnes AI provides free text-to-image generation.
    """

    def __init__(self, config: EngineConfig | None = None) -> None:
        if config is None:
            config = EngineConfig(
                provider="agnes_ai",
                model="agnes-image",
                api_key=None,
                timeout=60.0,
            )
        super().__init__(config)
        self.base_url = "https://api.agnes-ai.com/v1"

    async def initialize(self) -> None:
        """Initialize the Agnes image engine."""
        self._state = EngineState.LOADING
        if not self._config.api_key:
            logger.warning("No API key provided for Agnes AI")
        self._state = EngineState.READY
        logger.info("Agnes image engine initialized")

    async def generate_image(
        self,
        prompt: str,
        config: ImageConfig | None = None,
    ) -> bytes:
        """Generate image using Agnes AI.

        Parameters
        ----------
        prompt:
            Text description of the image.
        config:
            Image generation configuration.

        Returns
        -------
        bytes
            Generated image data.
        """
        config = config or self.image_config
        self._state = EngineState.GENERATING

        headers = {
            "Authorization": f"Bearer {self._config.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "prompt": prompt,
            "width": config.width,
            "height": config.height,
            "steps": config.steps,
            "guidance_scale": config.guidance_scale,
        }
        if config.seed is not None:
            payload["seed"] = config.seed
        if config.negative_prompt:
            payload["negative_prompt"] = config.negative_prompt

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/images/generate",
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
                    image_url = result.get("image_url") or result.get("url")

                    if not image_url:
                        raise AIEngineError(
                            "No image URL in response",
                            provider=self._config.provider,
                        )

                    async with session.get(image_url) as img_response:
                        image_data = await img_response.read()

                    self._record_success()
                    self._state = EngineState.READY
                    return image_data
        except AIEngineError:
            raise
        except Exception as exc:
            self._state = EngineState.ERROR
            raise AIEngineError(
                f"Agnes image generation failed: {exc}",
                provider=self._config.provider,
            ) from exc
