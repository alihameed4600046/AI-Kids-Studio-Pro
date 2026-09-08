"""Tests for the AI Engine framework."""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

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
from src.prompt.template_registry import TemplateDefinition, TemplateRegistry

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

    def test_load_yaml_mapping_template(self, tmp_path: Path) -> None:
        engine = PromptEngine(prompts_dir=tmp_path)
        template_file = tmp_path / "greeting.yaml"
        template_file.write_text('prompt: "Hello {{name}}!"', encoding="utf-8")
        result = engine.load_template("greeting")
        assert result == '"Hello {{name}}!"'

    def test_load_plain_text_template(self, tmp_path: Path) -> None:
        engine = PromptEngine(prompts_dir=tmp_path)
        template_file = tmp_path / "plain.yaml"
        template_file.write_text("Hello {{name}}!", encoding="utf-8")
        result = engine.load_template("plain")
        assert result == "Hello {{name}}!"

    def test_load_missing_template_raises(self, tmp_path: Path) -> None:
        engine = PromptEngine(prompts_dir=tmp_path)
        with pytest.raises(PromptTemplateError, match="Template not found"):
            engine.load_template("nonexistent")

    def test_load_malformed_yaml_raises(self, tmp_path: Path) -> None:
        engine = PromptEngine(prompts_dir=tmp_path)
        template_file = tmp_path / "bad.yaml"
        template_file.write_text("prompt: Hello {{name}}!\nThis line has no colon", encoding="utf-8")
        with pytest.raises(PromptTemplateError, match="Failed to parse template"):
            engine.load_template("bad")

    def test_render_substitutes_variables(self, tmp_path: Path) -> None:
        engine = PromptEngine(prompts_dir=tmp_path)
        template_file = tmp_path / "greeting.yaml"
        template_file.write_text('prompt: "Hello {{name}}!"', encoding="utf-8")
        result = engine.render("greeting", {"name": "Alice"})
        assert result == '"Hello Alice!"'

    def test_build_request_uses_rendered_prompt(self, tmp_path: Path) -> None:
        engine = PromptEngine(prompts_dir=tmp_path)
        template_file = tmp_path / "greeting.yaml"
        template_file.write_text('prompt: "Hello {{name}}!"', encoding="utf-8")
        request = engine.build_request("greeting", {"name": "Alice"})
        assert request.prompt == '"Hello Alice!"'


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

    @pytest.mark.asyncio
    async def test_generate_raises_clear_error_when_no_providers_enabled(
        self,
    ) -> None:
        """Zero enabled providers produces a clear error, not 'Last error: None'."""
        manager = ModelManager()
        request = GenerationRequest(prompt="Hello")
        with pytest.raises(AIEngineError, match="No providers available"):
            await manager.generate(request)

    @pytest.mark.asyncio
    async def test_generate_preserves_all_failed_error_when_providers_exhausted(
        self,
    ) -> None:
        """When providers exist but all fail, the existing 'All providers failed' message is preserved."""
        manager = ModelManager()
        failing_engine = MagicMock()
        failing_engine.is_ready = True
        failing_engine.state = EngineState.READY
        failing_engine.initialize = AsyncMock()
        failing_engine.generate = AsyncMock(
            side_effect=AIEngineError("mock provider failure", provider="mock")
        )
        failing_engine.shutdown = AsyncMock()

        manager.register_provider(
            ProviderConfig(
                provider_type=ProviderType.MOCK,
                enabled=True,
                priority=1,
                metadata={"supported_tasks": ["text_generation"]},
            )
        )
        manager.register_engine(ProviderType.MOCK, failing_engine)

        request = GenerationRequest(prompt="Hello")
        with pytest.raises(AIEngineError, match="All providers failed"):
            await manager.generate(request)


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


class TestPromptEngineTemplateRegistryBridge:
    """Tests for PromptEngine integration with TemplateRegistry."""

    def _make_registry(self) -> TemplateRegistry:
        registry = TemplateRegistry()
        registry.register(
            TemplateDefinition(
                name="Test Builtin",
                category="Education",
                description="A test builtin template.",
                template="Hello {{name}}, welcome to {{place}}!",
                variables=["name", "place"],
            )
        )
        return registry

    def test_load_builtin_template_without_yaml(self) -> None:
        """Builtin TemplateRegistry templates are available without YAML files."""
        registry = self._make_registry()
        engine = PromptEngine(template_registry=registry)

        result = engine.load_template("Test Builtin")
        assert result == "Hello {{name}}, welcome to {{place}}!"

    def test_render_builtin_template_with_variables(self) -> None:
        """Builtin templates can be rendered with variable substitution."""
        registry = self._make_registry()
        engine = PromptEngine(template_registry=registry)
        engine.set_variables({"name": "Alice", "place": "Wonderland"})

        result = engine.render("Test Builtin")
        assert result == "Hello Alice, welcome to Wonderland!"

    def test_yaml_template_still_works_when_not_in_registry(self, tmp_path: Path) -> None:
        """YAML loading is preserved for templates not provided by the registry."""
        yaml_file = tmp_path / "custom.yaml"
        yaml_file.write_text('prompt: "YAML {{value}} content"', encoding="utf-8")
        engine = PromptEngine(prompts_dir=tmp_path)

        result = engine.load_template("custom")
        assert result == '"YAML {{value}} content"'

    def test_registry_template_takes_precedence_over_yaml(self, tmp_path: Path) -> None:
        """In-memory registry templates take precedence over YAML files."""
        registry = self._make_registry()
        yaml_file = tmp_path / "Test Builtin.yaml"
        yaml_file.write_text('prompt: "YAML version"', encoding="utf-8")
        engine = PromptEngine(prompts_dir=tmp_path, template_registry=registry)

        result = engine.load_template("Test Builtin")
        assert result == "Hello {{name}}, welcome to {{place}}!"

    def test_prompt_engine_without_registry_unchanged(self) -> None:
        """PromptEngine without a registry behaves exactly as before."""
        engine = PromptEngine()
        assert engine._template_registry is None
        assert engine.templates == {}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
