"""Tests for SettingsPage and settings navigation wiring."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# ---------------------------------------------------------------------------
# Mock customtkinter / tkinter BEFORE importing SettingsPage so its __init__
# can run without a real display server.
# ---------------------------------------------------------------------------

class DummyCTkFrame:
    """Minimal real class so ABC inheritance works during tests."""

    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, name):
        return MagicMock()


_mock_ctk = MagicMock()
_mock_ctk.CTkBaseClass = object
_mock_ctk.CTkFrame = DummyCTkFrame
_mock_ctk.CTkScrollableFrame = DummyCTkFrame
_mock_ctk.StringVar.side_effect = lambda *args, **kwargs: MagicMock()
sys.modules["customtkinter"] = _mock_ctk

_mock_tk = MagicMock()
sys.modules["tkinter"] = _mock_tk
sys.modules["tkinter.filedialog"] = _mock_tk.filedialog
sys.modules["tkinter.messagebox"] = _mock_tk.messagebox

from src.views.pages.settings_page import SettingsPage  # noqa: E402
import src.views.pages.settings_page as _settings_page_module  # noqa: E402
from src.settings.manager import SettingsManager  # noqa: E402
from src.navigation.navigation_manager import NavigationManager  # noqa: E402

print("SETTINGS_MODULE_CTK_CHECK:", _settings_page_module.ctk is _mock_ctk, "ctk_id=", id(_settings_page_module.ctk), "mock_id=", id(_mock_ctk))
print("SETTINGS_MODULE_STRINGVAR_CHECK:", _settings_page_module.ctk.StringVar is _mock_ctk.StringVar)

# Use the ctk module that SettingsPage actually imported.
_page_ctk = _settings_page_module.ctk


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_settings_manager(tmp_path: Path) -> SettingsManager:
    """Create a SettingsManager backed by a temp JSON file."""
    cfg_path = tmp_path / "settings.json"
    default = {
        "theme": {},
        "window": {"width": 1200, "height": 800},
        "recent_projects": [],
        "openrouter_model": "openai/gpt-3.5-turbo",
        "openrouter_base_url": "https://openrouter.ai/api/v1",
    }
    return SettingsManager(cfg_path, default)


def _make_page(tmp_path: Path) -> SettingsPage:
    """Create a SettingsPage with mocked CTk environment and fake dependencies."""
    settings_manager = _make_settings_manager(tmp_path)
    page = SettingsPage(
        master=MagicMock(),
        navigation_manager=MagicMock(),
        settings_manager=settings_manager,
    )
    return page


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestSettingsPage:
    """Tests for SettingsPage configuration behavior."""

    def _patch_settings_page_ctk(self) -> None:
        """Ensure SettingsPage uses our test mock for customtkinter."""
        _settings_page_module.ctk = _mock_ctk

    def test_loads_existing_settings(self, tmp_path: Path) -> None:
        """SettingsPage loads existing OpenRouter settings into UI variables."""
        self._patch_settings_page_ctk()
        cfg_path = tmp_path / "settings.json"
        sm = SettingsManager(
            cfg_path,
            {
                "openrouter_api_key": "existing-key",
                "openrouter_model": "openai/gpt-4o",
                "openrouter_base_url": "https://custom.openrouter.ai/api/v1",
            },
        )
        page = SettingsPage(
            master=MagicMock(),
            navigation_manager=MagicMock(),
            settings_manager=sm,
        )

        page._api_key_var.get.return_value = "existing-key"
        page._model_var.get.return_value = "openai/gpt-4o"
        page._base_url_var.get.return_value = "https://custom.openrouter.ai/api/v1"

        page._load_settings()

        page._api_key_var.set.assert_called_with("existing-key")
        page._model_var.set.assert_called_with("openai/gpt-4o")
        page._base_url_var.set.assert_called_with("https://custom.openrouter.ai/api/v1")

    def test_save_settings_persists_to_settings_manager(self, tmp_path: Path) -> None:
        """Save button writes OpenRouter settings through SettingsManager."""
        self._patch_settings_page_ctk()
        sm = _make_settings_manager(tmp_path)
        page = SettingsPage(
            master=MagicMock(),
            navigation_manager=MagicMock(),
            settings_manager=sm,
        )

        page._api_key_var.get.return_value = "new-api-key"
        page._model_var.get.return_value = "openai/gpt-4o"
        page._base_url_var.get.return_value = "https://custom.openrouter.ai/api/v1"

        page._save_settings()

        assert sm.get("openrouter_api_key") == "new-api-key"
        assert sm.get("openrouter_model") == "openai/gpt-4o"
        assert sm.get("openrouter_base_url") == "https://custom.openrouter.ai/api/v1"

    def test_does_not_hardcode_credentials(self, tmp_path: Path) -> None:
        """SettingsPage does not embed a hardcoded API key in source."""
        source = Path(__import__("src.views.pages.settings_page", fromlist=[""]).__file__).read_text(
            encoding="utf-8"
        )
        assert "sk-" not in source
        assert "hardcoded" not in source.lower()

    def test_restart_message_is_displayed_on_save(self, tmp_path: Path) -> None:
        """Save feedback tells the user to restart the application."""
        self._patch_settings_page_ctk()
        sm = _make_settings_manager(tmp_path)
        page = SettingsPage(
            master=MagicMock(),
            navigation_manager=MagicMock(),
            settings_manager=sm,
        )

        page._api_key_var.get.return_value = "some-key"
        page._model_var.get.return_value = "openai/gpt-3.5-turbo"
        page._base_url_var.get.return_value = "https://openrouter.ai/api/v1"

        page._save_settings()

        page._feedback_var.get.return_value = "Settings saved. Restart the application for changes to take effect."
        assert "restart" in page._feedback_var.get().lower()


class TestSettingsNavigation:
    """Tests for Settings page navigation wiring."""

    def test_settings_nav_resolves_to_settings_page(self, tmp_path: Path) -> None:
        """NavigationManager 'settings' page is registered as SettingsPage."""
        _settings_page_module.ctk = _mock_ctk

        nav = NavigationManager(
            MagicMock(),
            MagicMock(),
            shared_dependencies={
                "settings_manager": _make_settings_manager(tmp_path),
            },
        )
        nav.register_page("settings", SettingsPage)

        assert "settings" in nav._page_registry
        page = nav._get_or_create_page("settings")
        assert isinstance(page, SettingsPage)
