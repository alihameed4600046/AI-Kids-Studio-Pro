"""Tests for PromptsPage generation integration."""

from __future__ import annotations

import asyncio
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Mock customtkinter / tkinter BEFORE importing PromptsPage so its __init__
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
sys.modules.setdefault("customtkinter", _mock_ctk)

_mock_tk = MagicMock()
sys.modules.setdefault("tkinter", _mock_tk)
sys.modules.setdefault("tkinter.filedialog", _mock_tk.filedialog)
sys.modules.setdefault("tkinter.messagebox", _mock_tk.messagebox)

from src.views.pages.prompts_page import PromptsPage  # noqa: E402
from src.services.generation_service import (  # noqa: E402
    GenerationJob,
    GenerationService,
    GenerationStatus,
    MediaType,
)
from src.engine.ai_engine import GenerationResponse  # noqa: E402
from src.engine.mock_engine import MockModelManager  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_completed_job(response_text: str = "mock response") -> GenerationJob:
    job = GenerationJob(
        id="job-123",
        category="stories",
        template_name="story",
        variables={"name": "Alice"},
        media_types=[MediaType.TEXT],
        status=GenerationStatus.COMPLETED,
        result=GenerationResponse(
            text=response_text,
            model="mock",
            provider="mock",
        ),
        error=None,
    )
    job.completed_at = None
    job.duration_ms = 100.0
    return job


def _make_page(tmp_path: Path) -> PromptsPage:
    """Create a PromptsPage with mocked CTk environment and fake dependencies."""
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)

    prompt_service = MagicMock()
    template_registry = MagicMock()
    variable_registry = MagicMock()
    generation_service = MagicMock(spec=GenerationService)

    page = PromptsPage(
        master=MagicMock(),
        navigation_manager=MagicMock(),
        prompt_service=prompt_service,
        template_registry=template_registry,
        variable_registry=variable_registry,
        generation_service=generation_service,
    )
    page._collect_variable_values = MagicMock(return_value={})
    return page


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestPromptsPageGeneration:
    """Integration tests for PromptsPage generation wiring."""

    def test_generate_button_is_wired(self, tmp_path: Path) -> None:
        """Generate button command is bound to _on_generate_clicked."""
        page = _make_page(tmp_path)
        call_args = _mock_ctk.CTkButton.call_args
        assert call_args is not None
        _, kwargs = call_args
        assert kwargs.get("command") == page._on_generate_clicked

    def test_on_generate_clicked_success(self, tmp_path: Path) -> None:
        """Successful generation calls display_response via after()."""
        page = _make_page(tmp_path)

        page._template_editor.get.return_value = "Hello {{name}}!"
        page._collect_variable_values.return_value = {"name": "Alice"}
        page._category_var.get.return_value = "stories"
        page._template_var.get.return_value = "story"

        job = _make_completed_job("Once upon a time...")
        page._generation_service.create_job.return_value = job
        page._generation_service.execute_job.return_value = job

        page._set_generating_state = MagicMock()

        def _after(delay, callback, *args):
            callback(*args)

        page.after = _after

        asyncio.run(page.on_generate_clicked("stories", "story", {"name": "Alice"}))

        page._generation_service.create_job.assert_called_once_with(
            category="stories",
            template_name="story",
            variables={"name": "Alice"},
            media_types=[MediaType.TEXT],
        )
        page._generation_service.execute_job.assert_called_once_with(job)
        page._set_generating_state.assert_called_with(False)
        page._result_textbox.delete.assert_called_with("1.0", "end")
        page._result_textbox.insert.assert_called_with("1.0", "Once upon a time...")

    def test_on_generate_clicked_failure(self, tmp_path: Path) -> None:
        """Failed generation routes to show_error."""
        page = _make_page(tmp_path)

        page._template_editor.get.return_value = "Hello {{name}}!"
        page._collect_variable_values.return_value = {"name": "Alice"}
        page._category_var.get.return_value = "stories"
        page._template_var.get.return_value = "story"

        page._generation_service.create_job.side_effect = RuntimeError("API down")

        page._set_generating_state = MagicMock()

        def _after(delay, callback, *args):
            callback(*args)

        page.after = _after

        asyncio.run(page.on_generate_clicked("stories", "story", {"name": "Alice"}))

        page._generation_service.create_job.assert_called_once()
        page._set_generating_state.assert_called_with(False)
        page._result_textbox.delete.assert_called_with("1.0", "end")
        page._result_textbox.insert.assert_called_with(
            "1.0", "Error: API down"
        )

    def test_display_response(self, tmp_path: Path) -> None:
        """display_response writes text into the result textbox."""
        page = _make_page(tmp_path)
        page.display_response("generated text")
        page._result_textbox.configure.assert_any_call(state="normal")
        page._result_textbox.delete.assert_called_with("1.0", "end")
        page._result_textbox.insert.assert_called_with("1.0", "generated text")
        page._result_textbox.configure.assert_any_call(state="disabled")

    def test_show_error(self, tmp_path: Path) -> None:
        """show_error writes error text and shows messagebox."""
        page = _make_page(tmp_path)
        error = ValueError("something failed")
        page.show_error(error)
        page._result_textbox.configure.assert_any_call(state="normal")
        page._result_textbox.delete.assert_called_with("1.0", "end")
        page._result_textbox.insert.assert_called_with("1.0", "Error: something failed")
        page._result_textbox.configure.assert_any_call(state="disabled")
        _mock_tk.messagebox.showerror.assert_called_with(
            "Generation Error", "something failed"
        )

    def test_set_generating_state(self, tmp_path: Path) -> None:
        """_set_generating_state toggles the generate button."""
        page = _make_page(tmp_path)
        page._set_generating_state(True)
        page._generate_button.configure.assert_called_with(
            state="disabled", text="Generating..."
        )
        page._generate_button.update_idletasks.assert_called()

        page._set_generating_state(False)
        page._generate_button.configure.assert_called_with(
            state="normal", text="Generate"
        )

    def test_generate_empty_template_warning(self, tmp_path: Path) -> None:
        """Empty template shows warning and does not start generation."""
        page = _make_page(tmp_path)
        page._template_editor.get.return_value = ""
        page._on_generate_clicked()
        _mock_tk.messagebox.showwarning.assert_called_with(
            "Generate", "Please enter or select a prompt template."
        )
        page._generation_service.create_job.assert_not_called()

    def test_generate_prevents_duplicate(self, tmp_path: Path) -> None:
        """Already-running generation shows warning."""
        page = _make_page(tmp_path)
        page._template_editor.get.return_value = "template"
        page._collect_variable_values.return_value = {}
        page._category_var.get.return_value = "stories"
        page._template_var.get.return_value = "story"

        fake_thread = MagicMock()
        fake_thread.is_alive.return_value = True
        page._generation_thread = fake_thread

        page._on_generate_clicked()
        _mock_tk.messagebox.showwarning.assert_called_with(
            "Generate", "Generation is already in progress."
        )
        page._generation_service.create_job.assert_not_called()

    def test_generate_thread_wiring(self, tmp_path: Path) -> None:
        """_on_generate_clicked starts a daemon thread with asyncio.run."""
        page = _make_page(tmp_path)
        page._template_editor.get.return_value = "template"
        page._collect_variable_values.return_value = {}
        page._category_var.get.return_value = "stories"
        page._template_var.get.return_value = "story"

        job = _make_completed_job("ok")
        page._generation_service.create_job.return_value = job
        page._generation_service.execute_job.return_value = job

        captured: dict = {}

        class FakeThread:
            def __init__(self, target=None, daemon=False, **kwargs):
                captured["target"] = target
                captured["daemon"] = daemon
                self._target = target

            def start(self):
                if self._target:
                    self._target()

            def is_alive(self):
                return False

        with patch("threading.Thread", FakeThread):
            page._on_generate_clicked()

        assert captured["daemon"] is True
        assert captured["target"] is not None
        assert page._generation_service.create_job.called
