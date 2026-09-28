"""Focused tests for MainWindow media-engine composition."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from src.engine.voice_engine import EdgeTTSEngine
from src.engine.video_engine import MockVideoEngine
from src.views.main_window import MainWindow


def test_main_window_wires_media_engines_to_ui_generation_service() -> None:
    """MainWindow attaches voice/video engines to the service passed to navigation."""
    bootstrap = MagicMock()
    config = MagicMock()
    config.get.side_effect = lambda _section, _key, default=None: default
    bootstrap.config = config
    bootstrap.model_manager = MagicMock()
    bootstrap.theme_manager = MagicMock()
    bootstrap.settings_manager = MagicMock()
    bootstrap.settings_manager.get.return_value = {
        "width": 1200,
        "height": 800,
    }
    bootstrap.generation_service.repository = MagicMock()

    generation_service = MagicMock()

    with (
        patch("src.views.main_window.ctk.CTk.__init__", return_value=None),
        patch("src.views.main_window.ctk.CTk.title"),
        patch("src.views.main_window.ctk.CTk.geometry"),
        patch("src.views.main_window.ctk.CTk.minsize"),
        patch("src.views.main_window.ctk.CTk.update_idletasks"),
        patch("src.views.main_window.ctk.CTk.protocol"),
        patch("src.views.main_window.get_logger", return_value=MagicMock()),
        patch("src.views.main_window.ProjectService", return_value=MagicMock()),
        patch("src.views.main_window.VariableRegistry", return_value=MagicMock()),
        patch("src.views.main_window.TemplateRegistry", return_value=MagicMock()),
        patch("src.views.main_window.GenerationService", return_value=generation_service),
        patch("src.views.main_window.NavigationManager") as navigation_manager_cls,
        patch.object(MainWindow, "_center_window"),
        patch.object(MainWindow, "_apply_theme"),
        patch.object(MainWindow, "_setup_layout"),
        patch.object(
            MainWindow,
            "_create_containers",
            lambda self: setattr(self, "content_container", MagicMock()),
        ),
        patch.object(MainWindow, "_bind_events"),
        patch.object(MainWindow, "_refresh_project_dashboard"),
        patch.object(MainWindow, "_refresh_recent_projects"),
    ):
        MainWindow(bootstrap, config=config)

    generation_service.set_voice_engine.assert_called_once()
    generation_service.set_video_engine.assert_called_once()
    generation_service.set_image_engine.assert_not_called()
    assert isinstance(
        generation_service.set_voice_engine.call_args.args[0], EdgeTTSEngine
    )
    assert isinstance(
        generation_service.set_video_engine.call_args.args[0], MockVideoEngine
    )
    navigation_manager_cls.assert_called_once()
    shared_dependencies = navigation_manager_cls.call_args.kwargs["shared_dependencies"]
    assert shared_dependencies["generation_service"] is generation_service
