"""Tests for the AI Engine framework."""

from __future__ import annotations

import asyncio
import logging

import pytest

from src.engine.ai_engine import (
    AIEngineError,
    EngineConfig,
    EngineState,
    GenerationRequest,
    GenerationResponse,
    RetryStrategy,
)
from src.engine.mock_engine import MockEngine, MockModelManager, MockScenario
from src.engine.model_manager import ModelManager, ProviderConfig, ProviderType, TaskType
from src.engine.prompt_engine import PromptEngine, PromptTemplateError

logging.basicConfig(level=logging.DEBUG)


class TestPromptEngine:
    """Tests for PromptEngine."""

    def test_substitute_basic(self) -> None:
        engine = PromptEngine()
        engine.set_variables({"name": "Alice", "age": "10"})
        result = engine.substitute("Hello {{name}}, you are {{age}} years old!")
        assert result == "Hello Alice, you are 10 years old!"

    def test_substitute_missing_variable_raises(self) -> None:
        engine = PromptEngine()
        engine.set_variables({"name": "Alice"})
        with pytest.raises(PromptTemplateError, match="Missing variable"):
            engine.substitute("Hello {{name}}, you are {{age}} years old!")

    def test_extract_variables(self) -> None:
        engine = PromptEngine()
        template = "Hello {{name}}, you are {{age}} years old!"
        variables = engine.extract_variables(template)
        assert variables == ["name", "age"]

    def test_clear_variables(self) -> None:
        engine = PromptEngine()
        engine.set_variables({"name": "Alice"})
        engine.clear_variables()
        assert len(engine.variables) == 0


class TestMockEngine:
    """Tests for MockEngine."""

    @pytest.fixture
    def engine(self) -> MockEngine:
        return MockEngine()

    @pytest.mark.asyncio
    async def test_initialize(self, engine: MockEngine) -> None:
        await engine.initialize()
        assert engine.state == EngineState.READY
        assert engine.is_ready

    @pytest.mark.asyncio
    async def test_generate_success(self, engine: MockEngine) -> None:
        await engine.initialize()
        request = GenerationRequest(prompt="Hello")
        response = await engine.generate(request)
        assert response.text == "This is a mock response from the AI engine."
        assert response.provider == "mock"
        assert response.tokens_used > 0

    @pytest.mark.asyncio
    async def test_generate_rate_limit(self, engine: MockEngine) -> None:
        engine.set_scenario(MockScenario.RATE_LIMIT)
        await engine.initialize()
        request = GenerationRequest(prompt="Hello")
        with pytest.raises(Exception, match="rate limit"):
            await engine.generate(request)

    @pytest.mark.asyncio
    async def test_stream(self, engine: MockEngine) -> None:
        engine.set_scenario(MockScenario.STREAM_SUCCESS)
        await engine.initialize()
        request = GenerationRequest(prompt="Hello")
        chunks = []
        async for chunk in engine.stream(request):
            chunks.append(chunk)
        assert len(chunks) > 0
        assert "".join(chunks) == "This is a mock response from the AI engine."

    @pytest.mark.asyncio
    async def test_retry_logic(self, engine: MockEngine) -> None:
        engine.config.max_retries = 2
        engine.config.retry_strategy = RetryStrategy.FIXED_DELAY
        engine.config.retry_delay = 0.01
        engine.set_scenario(MockScenario.RATE_LIMIT)
        await engine.initialize()
        request = GenerationRequest(prompt="Hello")
        with pytest.raises(Exception, match="rate limit"):
            await engine.generate(request)
        assert engine.call_count == 3  # initial + 2 retries


class TestModelManager:
    """Tests for ModelManager."""

    @pytest.fixture
    def manager(self) -> ModelManager:
        manager = ModelManager()
        config = ProviderConfig(
            provider_type=ProviderType.MOCK,
            enabled=True,
            priority=1,
            rate_limit_rpm=100,
            quota_requests=1000,
            quota_tokens=100000,
        )
        manager.register_provider(config)
        mock_engine = MockEngine()
        manager.register_engine(ProviderType.MOCK, mock_engine)
        return manager

    @pytest.mark.asyncio
    async def test_generate_with_mock(self, manager: ModelManager) -> None:
        await manager._engines[ProviderType.MOCK].initialize()
        request = GenerationRequest(prompt="Hello")
        response = await manager.generate(request, provider_type=ProviderType.MOCK)
        assert response.text is not None
        assert response.provider == "mock"

    def test_get_available_providers(self, manager: ModelManager) -> None:
        providers = manager.get_available_providers()
        assert "mock" in providers

    def test_get_provider_status(self, manager: ModelManager) -> None:
        status = manager.get_provider_status()
        assert "mock" in status
        assert "enabled" in status["mock"]


class TestMockModelManager:
    """Tests for MockModelManager."""

    @pytest.fixture
    def manager(self) -> MockModelManager:
        return MockModelManager()

    @pytest.mark.asyncio
    async def test_initialize(self, manager: MockModelManager) -> None:
        await manager.initialize()
        assert manager.mock_engine.is_ready

    @pytest.mark.asyncio
    async def test_generate(self, manager: MockModelManager) -> None:
        await manager.initialize()
        request = GenerationRequest(prompt="Hello")
        response = await manager.generate(request)
        assert response.text is not None

    @pytest.mark.asyncio
    async def test_stream(self, manager: MockModelManager) -> None:
        manager.set_scenario(MockScenario.STREAM_SUCCESS)
        await manager.initialize()
        request = GenerationRequest(prompt="Hello")
        chunks = []
        async for chunk in manager.stream(request):
            chunks.append(chunk)
        assert len(chunks) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
