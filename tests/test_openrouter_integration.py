"""Integration tests for OpenRouter engine wiring through the application bootstrap.

These tests verify the end-to-end runtime flow:

    UI / PromptsPage
      -> GenerationService (from bootstrap)
      -> ModelManager (from bootstrap)
      -> OpenRouterEngine (registered via bootstrap)
      -> OpenRouter API (mocked – no real network calls)

All singletons (DatabaseManager, ProjectManager, SettingsManager, ThemeManager)
are reset before and after each test to avoid cross-test contamination.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
import yaml

from config.config import Config
from src.bootstrap import ApplicationBootstrap
from src.database.database_manager import DatabaseManager
from src.engine.ai_engine import GenerationRequest
from src.engine.model_manager import ModelManager, ProviderConfig, ProviderType, TaskType
from src.engine.openrouter_engine import OpenRouterEngine
from src.project.project_manager import ProjectManager
from src.services.generation_service import GenerationService
from src.settings.manager import SettingsManager
from src.theme.theme_manager import ThemeManager


def _make_mock_response(
    status: int = 200,
    response_data: dict | None = None,
    headers: dict | None = None,
) -> MagicMock:
    mock_response = MagicMock()
    mock_response.status = status
    mock_response.headers = headers or {}
    mock_response.text = AsyncMock(return_value=json.dumps(response_data or {}))
    mock_response.json = AsyncMock(return_value=response_data or {})
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=False)
    return mock_response


@pytest.fixture
def temp_app(tmp_path: Path) -> Path:
    """Create a fully-isolated temporary application environment.

    Writes a *config.yaml* and *settings.json* in *tmp_path* with OpenRouter
    credentials, resets all known singletons, and yields the temp directory.
    Singletons are reset again on teardown.
    """
    config_data = {
        "log": {"level": "INFO", "file": str(tmp_path / "logs" / "app.log")},
        "paths": {
            "root": str(tmp_path),
            "settings": str(tmp_path / "settings.json"),
            "theme": str(tmp_path / "theme.json"),
        },
        "database": {"path": str(tmp_path / "test.db")},
    }
    (tmp_path / "config.yaml").write_text(yaml.safe_dump(config_data), encoding="utf-8")

    settings_data = {
        "openrouter_api_key": "test-openrouter-key",
        "openrouter_model": "openai/gpt-4o",
        "openrouter_base_url": "https://openrouter.ai/api/v1",
        "theme": {},
        "window": {"width": 1200, "height": 800},
        "recent_projects": [],
    }
    (tmp_path / "settings.json").write_text(
        json.dumps(settings_data), encoding="utf-8"
    )

    # Reset singletons so each test gets a fresh instance tied to temp paths.
    DatabaseManager._instance = None
    ProjectManager._instance = None
    SettingsManager._instance = None
    ThemeManager._instance = None

    yield tmp_path

    DatabaseManager._instance = None
    ProjectManager._instance = None
    SettingsManager._instance = None
    ThemeManager._instance = None


class TestBootstrapOpenRouterIntegration:
    """Integration tests for OpenRouter engine wiring via the bootstrap."""

    def test_bootstrap_registers_openrouter(self, temp_app: Path) -> None:
        """Bootstrap creates and registers the OpenRouter provider and engine."""
        bootstrap = ApplicationBootstrap(temp_app / "config.yaml")
        bootstrap.initialize()

        try:
            mm = bootstrap.model_manager

            provider = mm.registry.get(ProviderType.OPENROUTER)
            assert provider is not None
            assert provider.enabled
            assert provider.api_key == "test-openrouter-key"
            assert provider.base_url == "https://openrouter.ai/api/v1"
            assert "text_generation" in provider.metadata.get("supported_tasks", [])

            engine = mm._engines.get(ProviderType.OPENROUTER)
            assert engine is not None
            assert isinstance(engine, OpenRouterEngine)
        finally:
            bootstrap.shutdown()

    def test_generation_service_uses_bootstrap_model_manager(
        self, temp_app: Path
    ) -> None:
        """GenerationService uses the ModelManager created by bootstrap."""
        bootstrap = ApplicationBootstrap(temp_app / "config.yaml")
        bootstrap.initialize()

        try:
            gs = bootstrap.generation_service
            assert gs is not None
            assert gs.model_manager is bootstrap.model_manager
            assert ProviderType.OPENROUTER in gs.model_manager._engines
        finally:
            bootstrap.shutdown()

    @pytest.mark.asyncio
    async def test_model_manager_routes_to_openrouter(
        self, temp_app: Path
    ) -> None:
        """ModelManager.generate routes to OpenRouterEngine without real API calls."""
        bootstrap = ApplicationBootstrap(temp_app / "config.yaml")
        bootstrap.initialize()

        try:
            mm = bootstrap.model_manager
            engine = mm._engines[ProviderType.OPENROUTER]

            await engine.initialize()

            response_data = {
                "id": "gen-123",
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "Hello from OpenRouter!",
                        },
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "total_tokens": 10,
                    "prompt_tokens": 5,
                    "completion_tokens": 5,
                },
            }
            mock_response = _make_mock_response(200, response_data)
            mock_post = MagicMock(return_value=mock_response)

            with patch.object(engine._session, "post", mock_post):
                request = GenerationRequest(prompt="Say hello")
                response = await mm.generate(
                    request, provider_type=ProviderType.OPENROUTER
                )

            assert response.text == "Hello from OpenRouter!"
            assert response.provider == "openrouter"
            assert response.model == "openai/gpt-4o"
            # The mock was called exactly once, proving no real API call.
            mock_post.assert_called_once()

            await engine.shutdown()
        finally:
            bootstrap.shutdown()

    def test_openrouter_disabled_without_api_key(self, temp_app: Path) -> None:
        """OpenRouter is registered but disabled when no API key is configured."""
        settings_data = {
            "openrouter_model": "openai/gpt-4o",
            "theme": {},
            "window": {"width": 1200, "height": 800},
            "recent_projects": [],
        }
        (temp_app / "settings.json").write_text(
            json.dumps(settings_data), encoding="utf-8"
        )
        SettingsManager._instance = None

        bootstrap = ApplicationBootstrap(temp_app / "config.yaml")
        bootstrap.initialize()

        try:
            mm = bootstrap.model_manager
            provider = mm.registry.get(ProviderType.OPENROUTER)
            assert provider is not None
            assert not provider.enabled
        finally:
            bootstrap.shutdown()
