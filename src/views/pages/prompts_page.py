'''Prompt Editor page for AI Kids Studio Pro.

This module provides the PromptsPage class for managing prompt templates
with a live preview panel.
'''

from __future__ import annotations

import logging
from typing import Any, TYPE_CHECKING

import customtkinter as ctk
from tkinter import filedialog, messagebox

from src.prompt.prompt_service import PromptService
from src.prompt.template_registry import TemplateRegistry, TemplateDefinition
from src.prompt.variable_registry import VariableRegistry
from src.views.pages.base_page import BasePage

if TYPE_CHECKING:
    from src.navigation.navigation_manager import NavigationManager


__all__ = ['PromptsPage']


class PromptsPage(BasePage):
    '''Prompt Editor page with live preview functionality.'''

    def __init__(
        self,
        master: ctk.CTkBaseClass,
        navigation_manager: 'NavigationManager',
        prompt_service: PromptService | None = None,
        template_registry: TemplateRegistry | None = None,
        variable_registry: VariableRegistry | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, navigation_manager, **kwargs)
        self._prompt_service = prompt_service or PromptService()
        if template_registry is None:
            raise RuntimeError("TemplateRegistry dependency was not injected into PromptsPage.")
        self._template_registry = template_registry
        if variable_registry is None:
            raise RuntimeError("VariableRegistry dependency was not injected into PromptsPage.")
        self._variable_registry = variable_registry
        self._variable_widgets: dict[str, Any] = {}
        self._variable_widget_vars: dict[str, Any] = {}
        self._logger = logging.getLogger(f'page.{self.__class__.__name__}')
        self._selected_prompt_id: str | None = None
        self._selected_prompt: Any | None = None
        self._saved_prompts: list[Any] = []

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._create_toolbar()
        self._create_title_entry()
        self._create_template_editor()
        self._create_variables_entry()
        self._create_live_preview()

        self._load_categories()
        self._load_templates()
        self._load_saved_prompts()

        self._logger.info('PromptsPage initialized')

    def _create_toolbar(self) -> None:
        toolbar_frame = ctk.CTkFrame(self)
        toolbar_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=(10, 5))
        toolbar_frame.grid_columnconfigure(0, weight=0)
        toolbar_frame.grid_columnconfigure(1, weight=1)
        toolbar_frame.grid_columnconfigure(2, weight=0)
        toolbar_frame.grid_columnconfigure(3, weight=1)
        toolbar_frame.grid_columnconfigure(4, weight=0)
        toolbar_frame.grid_columnconfigure(5, weight=1)
        toolbar_frame.grid_columnconfigure(6, weight=0)
        toolbar_frame.grid_columnconfigure(7, weight=0)
        toolbar_frame.grid_columnconfigure(8, weight=0)
        toolbar_frame.grid_columnconfigure(9, weight=0)
        toolbar_frame.grid_columnconfigure(10, weight=0)

        ctk.CTkLabel(toolbar_frame, text='Category:').grid(row=0, column=0, padx=(10, 5), pady=10, sticky='w')
        self._category_var = ctk.StringVar()
        self._category_dropdown = ctk.CTkComboBox(
            toolbar_frame,
            variable=self._category_var,
            values=[],
            state='readonly',
            command=self._on_category_changed,
        )
        self._category_dropdown.grid(row=0, column=1, padx=(0, 10), pady=10, sticky='ew')

        ctk.CTkLabel(toolbar_frame, text='Template:').grid(row=0, column=2, padx=(10, 5), pady=10, sticky='w')
        self._template_var = ctk.StringVar()
        self._template_dropdown = ctk.CTkComboBox(
            toolbar_frame,
            variable=self._template_var,
            values=[],
            state='readonly',
            command=self._on_template_changed,
        )
        self._template_dropdown.grid(row=0, column=3, padx=(0, 10), pady=10, sticky='ew')

        ctk.CTkLabel(toolbar_frame, text='Saved Prompt:').grid(row=0, column=4, padx=(10, 5), pady=10, sticky='w')
        self._saved_prompt_var = ctk.StringVar()
        self._saved_prompt_dropdown = ctk.CTkComboBox(
            toolbar_frame,
            variable=self._saved_prompt_var,
            values=[],
            state='readonly',
            command=self._on_saved_prompt_changed,
        )
        self._saved_prompt_dropdown.grid(row=0, column=5, padx=(0, 10), pady=10, sticky='ew')

        self._new_button = ctk.CTkButton(toolbar_frame, text='New', width=80, command=self._on_new_clicked)
        self._new_button.grid(row=0, column=6, padx=(0, 5), pady=10)

        self._save_button = ctk.CTkButton(toolbar_frame, text='Save', width=80, command=self._on_save_clicked)
        self._save_button.grid(row=0, column=7, padx=(0, 5), pady=10)

        self._delete_button = ctk.CTkButton(toolbar_frame, text='Delete', width=80, command=self._on_delete_clicked)
        self._delete_button.grid(row=0, column=8, padx=(0, 5), pady=10)

        self._history_button = ctk.CTkButton(toolbar_frame, text='History', width=80, command=self._on_history_clicked)
        self._history_button.grid(row=0, column=9, padx=(0, 5), pady=10)

        self._export_button = ctk.CTkButton(toolbar_frame, text='Export', width=80, command=self._on_export_clicked)
        self._export_button.grid(row=0, column=10, padx=(0, 10), pady=10)

    def _create_title_entry(self) -> None:
        title_frame = ctk.CTkFrame(self)
        title_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=(5, 5))
        title_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(title_frame, text='Prompt Title:').grid(row=0, column=0, padx=(10, 5), pady=10, sticky='w')
        self._title_var = ctk.StringVar()
        self._title_entry = ctk.CTkEntry(title_frame, textvariable=self._title_var, placeholder_text='Enter prompt title...')
        self._title_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky='ew')

    def _create_template_editor(self) -> None:
        editor_frame = ctk.CTkFrame(self)
        editor_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=(5, 5))
        editor_frame.grid_rowconfigure(0, weight=1)
        editor_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(editor_frame, text='Prompt Template Editor:').grid(row=0, column=0, padx=10, pady=(10, 0), sticky='nw')
        self._template_editor = ctk.CTkTextbox(editor_frame, font=ctk.CTkFont(family='Consolas', size=12), wrap='word')
        self._template_editor.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='nsew')

    def _create_variables_entry(self) -> None:
        variables_frame = ctk.CTkFrame(self)
        variables_frame.grid(row=3, column=0, sticky='nsew', padx=10, pady=(5, 5))
        variables_frame.grid_columnconfigure(0, weight=1)
        variables_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            variables_frame,
            text='Variables',
            font=ctk.CTkFont(size=14, weight='bold'),
        ).grid(row=0, column=0, padx=10, pady=(10, 5), sticky='w')

        self._variables_container = ctk.CTkScrollableFrame(variables_frame, height=220)
        self._variables_container.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='nsew')
        self._variables_container.grid_columnconfigure(0, weight=1)

    def _clear_variable_fields(self) -> None:
        self._variable_widgets.clear()
        self._variable_widget_vars.clear()
        for child in self._variables_container.winfo_children():
            child.destroy()

    def _create_variable_widget(
        self,
        variable_name: str,
        definition: Any | None,
        value: str | None = None,
    ) -> None:
        current_value = value if value is not None else ''
        display_name = (
            definition.display_name
            if definition is not None
            else variable_name.replace('_', ' ').title()
        )
        control_type = definition.type if definition is not None else 'text'
        placeholder = definition.placeholder if definition is not None else f'Enter {display_name}'
        default_value = current_value or (definition.default_value if definition is not None else '')
        options = definition.options if definition is not None else []

        row = len(self._variable_widgets)
        if control_type == 'boolean':
            value_var = ctk.BooleanVar(value=str(default_value).lower() in ('true', '1', 'yes'))
            widget = ctk.CTkCheckBox(
                self._variables_container,
                text=display_name,
                variable=value_var,
                command=self._update_preview,
            )
            widget.grid(row=row, column=0, padx=10, pady=5, sticky='w', columnspan=2)
            self._variable_widget_vars[variable_name] = value_var
        else:
            ctk.CTkLabel(
                self._variables_container,
                text=display_name,
            ).grid(row=row, column=0, padx=(10, 5), pady=5, sticky='w')

            if control_type == 'dropdown':
                value_var = ctk.StringVar(value=str(default_value))
                widget = ctk.CTkComboBox(
                    self._variables_container,
                    variable=value_var,
                    values=options,
                    state='readonly',
                    command=lambda *_: self._update_preview(),
                )
                widget.set(str(default_value))
            elif control_type == 'textarea':
                widget = ctk.CTkTextbox(
                    self._variables_container,
                    font=ctk.CTkFont(family='Consolas', size=11),
                    wrap='word',
                    height=80,
                )
                if default_value:
                    widget.insert('1.0', str(default_value))
                widget.bind('<KeyRelease>', lambda event: self._update_preview())
                value_var = None
            else:
                value_var = ctk.StringVar(value=str(default_value))
                widget = ctk.CTkEntry(
                    self._variables_container,
                    textvariable=value_var,
                    placeholder_text=placeholder,
                )
                value_var.set(str(default_value))
                value_var.trace_add('write', lambda *_: self._update_preview())

            widget.grid(row=row, column=1, padx=(0, 10), pady=5, sticky='ew')
            self._variable_widget_vars[variable_name] = value_var

        self._variable_widgets[variable_name] = widget

    def _generate_variable_fields(
        self,
        variable_names: list[str],
        current_values: dict[str, str] | None = None,
    ) -> None:
        self._clear_variable_fields()
        current_values = current_values or {}
        unique_variable_names: list[str] = []
        for variable_name in variable_names:
            normalized = variable_name.strip()
            if normalized and normalized not in unique_variable_names:
                unique_variable_names.append(normalized)

        for variable_name in unique_variable_names:
            definition = self._variable_registry.get(variable_name)
            self._create_variable_widget(variable_name, definition, current_values.get(variable_name))

        for variable_name, value in current_values.items():
            if variable_name not in self._variable_widgets:
                self._create_variable_widget(variable_name, None, value)

    def _collect_variable_values(self) -> dict[str, str]:
        variables: dict[str, str] = {}
        for variable_name, widget in self._variable_widgets.items():
            value_var = self._variable_widget_vars.get(variable_name)
            if value_var is not None:
                var_value = value_var.get()
                if isinstance(var_value, bool):
                    value = 'true' if var_value else 'false'
                else:
                    value = str(var_value).strip()
            elif isinstance(widget, ctk.CTkTextbox):
                value = widget.get('1.0', 'end-1c').strip()
            else:
                value = str(widget.get()).strip()

            if value or value == 'false':
                variables[variable_name] = value
        return variables

    def _create_live_preview(self) -> None:
        preview_frame = ctk.CTkFrame(self)
        preview_frame.grid(row=4, column=0, sticky='nsew', padx=10, pady=(5, 10))
        preview_frame.grid_rowconfigure(0, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(preview_frame, text='Live Preview:').grid(row=0, column=0, padx=10, pady=(10, 0), sticky='nw')
        self._preview_textbox = ctk.CTkTextbox(preview_frame, font=ctk.CTkFont(family='Consolas', size=12), wrap='word', state='disabled')
        self._preview_textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='nsew')

    def _load_categories(self) -> None:
        """Load categories from TemplateRegistry and populate the category dropdown."""
        try:
            categories = self._template_registry.get_categories()
            self._logger.info('Loaded %d categories', len(categories))
            self._category_dropdown.configure(values=categories)
            if categories:
                self._category_var.set(categories[0])
                self._on_category_changed(categories[0])
            else:
                self._logger.warning('No categories available')
                self._category_dropdown.configure(values=['No categories available'])
                self._category_dropdown.configure(state='disabled')
                self._template_dropdown.configure(values=['No templates available'])
                self._template_dropdown.configure(state='disabled')
        except Exception as exc:
            self._logger.error('Failed to load categories: %s', exc)
            self._category_dropdown.configure(values=['Error loading categories'])
            self._category_dropdown.configure(state='disabled')
            self._template_dropdown.configure(values=['Error loading templates'])
            self._template_dropdown.configure(state='disabled')

    def _load_templates(self) -> None:
        """Load templates for the currently selected category."""
        category = self._category_var.get()
        if not category or category in ('No categories available', 'Error loading categories'):
            self._template_dropdown.configure(values=['No templates available'])
            self._template_dropdown.configure(state='disabled')
            return

        try:
            templates = self._template_registry.get_templates(category)
            template_names = [t.name for t in templates]
            self._logger.info('Loaded %d templates for category: %s', len(template_names), category)
            self._template_dropdown.configure(values=template_names)
            self._template_dropdown.configure(state='readonly')
            if template_names:
                self._template_var.set(template_names[0])
                self._on_template_changed(template_names[0])
            else:
                self._template_var.set('')
                self._template_editor.delete('1.0', 'end')
                self._clear_variable_fields()
                self._update_preview()
        except Exception as exc:
            self._logger.error('Failed to load templates for category %s: %s', category, exc)
            self._template_dropdown.configure(values=['Error loading templates'])
            self._template_dropdown.configure(state='disabled')

    def _load_saved_prompts(self, selected_prompt_id: str | None = None) -> None:
        try:
            prompts = self._prompt_service.list_prompts()
            self._saved_prompts = list(prompts or [])
            prompt_titles = [getattr(prompt, 'title', str(prompt)) for prompt in self._saved_prompts]
            self._saved_prompt_dropdown.configure(values=prompt_titles)

            if selected_prompt_id is not None:
                for prompt in self._saved_prompts:
                    if getattr(prompt, 'id', None) == selected_prompt_id:
                        self._saved_prompt_var.set(getattr(prompt, 'title', ''))
                        return
            if self._selected_prompt_id is not None:
                for prompt in self._saved_prompts:
                    if getattr(prompt, 'id', None) == self._selected_prompt_id:
                        self._saved_prompt_var.set(getattr(prompt, 'title', ''))
                        return
            self._saved_prompt_var.set('')
        except (ValueError, FileNotFoundError, Exception) as exc:
            self._show_error(exc)

    def _on_category_changed(self, category: str) -> None:
        """Handle category change - reload templates for the new category."""
        self._logger.debug('Category changed to: %s', category)
        self._load_templates()
        self._update_preview()

    def _on_template_changed(self, template_name: str) -> None:
        """Handle template selection - load template from registry and auto-fill form."""
        self._logger.debug('Template changed to: %s', template_name)
        category = self._category_var.get()
        if not category or category in ('No categories available', 'Error loading categories'):
            return

        try:
            template_def = self._template_registry.get_template(template_name)
            if template_def is None:
                self._logger.warning('Template not found: %s', template_name)
                self._template_editor.delete('1.0', 'end')
                self._clear_variable_fields()
                self._update_preview()
                return

            self._logger.info('Selected template: %s', template_name)
            self._template_editor.delete('1.0', 'end')
            self._template_editor.insert('1.0', template_def.template)
            self._title_var.set(template_def.name)
            variables = self._extract_variables(template_def.template)
            self._generate_variable_fields(variables)
            self._update_preview()
        except Exception as exc:
            self._logger.error('Failed to load template: %s', exc)

    def _on_saved_prompt_changed(self, prompt_title: str) -> None:
        if not prompt_title:
            return
        for prompt in self._saved_prompts:
            if getattr(prompt, 'title', None) == prompt_title:
                self._selected_prompt = prompt
                self._selected_prompt_id = getattr(prompt, 'id', None)
                self._populate_form(prompt)
                return

    def _on_new_clicked(self) -> None:
        self._logger.info('New button clicked')
        self._selected_prompt = None
        self._selected_prompt_id = None
        self._saved_prompt_var.set('')
        self._title_var.set('')
        self._category_var.set('')
        self._template_editor.delete('1.0', 'end')
        self._clear_variable_fields()
        self._update_preview()

    def _on_save_clicked(self) -> None:
        self._logger.info('Save button clicked')
        try:
            title = self._title_var.get().strip()
            category = self._category_var.get().strip() or 'general'
            template = self._template_editor.get('1.0', 'end-1c').strip()
            variables = self._collect_variable_values()

            if not title:
                raise ValueError('Prompt title is required.')
            if not template:
                raise ValueError('Prompt template is required.')

            if self._selected_prompt_id is None:
                prompt = self._prompt_service.create_prompt(title, category, template, variables)
                self._logger.info('Created prompt: %s', prompt.id)
                messagebox.showinfo('Success', 'Prompt created successfully.')
                self._clear_form()
            else:
                prompt = self._prompt_service.update_prompt(self._selected_prompt_id, title, category, template, variables)
                self._logger.info('Updated prompt: %s', prompt.id)
                messagebox.showinfo('Success', 'Prompt updated successfully.')

            preview_text = self._prompt_service.render_template(template, variables)
            self._prompt_service.add_to_history(preview_text, category, title)
            self._load_saved_prompts(selected_prompt_id=prompt.id)
            self._selected_prompt = prompt
            self._selected_prompt_id = getattr(prompt, 'id', None)
            self._update_preview()
        except KeyError as exc:
            self._show_error(FileNotFoundError(str(exc)))
        except ValueError as exc:
            self._show_error(exc)
        except FileNotFoundError as exc:
            self._show_error(exc)
        except Exception as exc:
            self._show_error(exc)

    def _on_delete_clicked(self) -> None:
        self._logger.info('Delete button clicked')
        try:
            if self._selected_prompt_id is None:
                raise ValueError('Select a prompt to delete.')

            prompt = self._selected_prompt or self._find_prompt_by_id(self._selected_prompt_id)
            title = getattr(prompt, 'title', None) or 'this prompt'
            if not messagebox.askyesno('Delete prompt', f'Delete prompt \'{title}\'?'):
                return

            deleted = self._prompt_service.delete_prompt(self._selected_prompt_id)
            if not deleted:
                raise FileNotFoundError('Prompt not found.')

            self._logger.info('Deleted prompt: %s', self._selected_prompt_id)
            messagebox.showinfo('Success', 'Prompt deleted successfully.')
            self._clear_form()
            self._selected_prompt = None
            self._selected_prompt_id = None
            self._load_saved_prompts()
        except KeyError as exc:
            self._show_error(FileNotFoundError(str(exc)))
        except ValueError as exc:
            self._show_error(exc)
        except FileNotFoundError as exc:
            self._show_error(exc)
        except Exception as exc:
            self._show_error(exc)

    def _extract_variables(self, template_text: str) -> list[str]:
        variables: list[str] = []
        start = 0
        while True:
            open_idx = template_text.find('{{', start)
            if open_idx == -1:
                break
            close_idx = template_text.find('}}', open_idx + 2)
            if close_idx == -1:
                break
            var_name = template_text[open_idx + 2 : close_idx].strip()
            if var_name and var_name not in variables:
                variables.append(var_name)
            start = close_idx + 2
        return variables

    def _populate_form(self, prompt: Any) -> None:
        self._selected_prompt = prompt
        self._selected_prompt_id = getattr(prompt, 'id', None)
        self._title_var.set(getattr(prompt, 'title', '') or '')
        self._category_var.set(getattr(prompt, 'category', '') or '')
        self._template_editor.delete('1.0', 'end')
        self._template_editor.insert('1.0', getattr(prompt, 'template', '') or '')
        self._generate_variable_fields(
            self._extract_variables(getattr(prompt, 'template', '') or ''),
            getattr(prompt, 'variables', {}) or {},
        )
        self._update_preview()

    def _clear_form(self) -> None:
        self._selected_prompt = None
        self._selected_prompt_id = None
        self._saved_prompt_var.set('')
        self._title_var.set('')
        self._category_var.set('')
        self._template_editor.delete('1.0', 'end')
        self._clear_variable_fields()
        self._update_preview()

    def _find_prompt_by_id(self, prompt_id: str | None) -> Any | None:
        if prompt_id is None:
            return None
        for prompt in self._saved_prompts:
            if getattr(prompt, 'id', None) == prompt_id:
                return prompt
        return None

    def _update_preview(self) -> None:
        template = self._template_editor.get('1.0', 'end-1c')
        variables = self._collect_variable_values()
        preview_text = self._prompt_service.render_template(template, variables)

        self._preview_textbox.configure(state='normal')
        self._preview_textbox.delete('1.0', 'end')
        self._preview_textbox.insert('1.0', preview_text)
        self._preview_textbox.configure(state='disabled')

    def on_show(self) -> None:
        super().on_show()
        self._logger.info('Prompts page displayed')
        self._update_preview()

    def on_hide(self) -> None:
        super().on_hide()
        self._logger.info('Prompts page hidden')

    def on_navigate_to(self, **kwargs: Any) -> None:
        super().on_navigate_to(**kwargs)
        self._logger.debug('Navigated to PromptsPage with params: %s', kwargs)

    def _on_export_clicked(self) -> None:
        self._logger.info('Export button clicked')
        self._preview_textbox.configure(state='normal')
        try:
            preview_text = self._preview_textbox.get('1.0', 'end-1c')
        finally:
            self._preview_textbox.configure(state='disabled')

        if not preview_text.strip():
            messagebox.showwarning('Export Prompt', 'The current preview is empty. Nothing to export.')
            return

        try:
            file_path = filedialog.asksaveasfilename(initialfile='prompt.txt', defaultextension='.txt', title='Export Prompt')
            if not file_path:
                return
            with open(file_path, 'w', encoding='utf-8') as file_handle:
                file_handle.write(preview_text)
            messagebox.showinfo('Export Prompt', f'Prompt exported successfully to {file_path}')
        except PermissionError as exc:
            messagebox.showerror('Export Prompt', f'Permission denied while saving the file: {exc}')
        except OSError as exc:
            messagebox.showerror('Export Prompt', f'Could not save the file: {exc}')

    def _on_history_clicked(self) -> None:
        self._logger.info('History button clicked')
        history = self._prompt_service.get_history()
        if not history:
            info_dialog = ctk.CTkToplevel(self)
            info_dialog.title('Prompt History')
            info_dialog.geometry('400x200')
            info_dialog.transient(self)
            info_dialog.grab_set()
            ctk.CTkLabel(info_dialog, text='No prompt history available yet.\\nRender some prompts to see history here.').grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
            ctk.CTkButton(info_dialog, text='Close', command=info_dialog.destroy).grid(row=1, column=0, padx=20, pady=(0, 20))
            return

        history_window = ctk.CTkToplevel(self)
        history_window.title('Prompt History')
        history_window.geometry('700x500')
        history_window.transient(self)
        history_window.grab_set()
        history_window.grid_rowconfigure(1, weight=1)
        history_window.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(history_window, text='Prompt History (Newest First)', font=ctk.CTkFont(size=14, weight='bold')).grid(row=0, column=0, padx=10, pady=(10, 5), sticky='w')
        list_frame = ctk.CTkScrollableFrame(history_window)
        list_frame.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
        list_frame.grid_columnconfigure(0, weight=1)

        preview_frame = ctk.CTkFrame(history_window)
        preview_frame.grid(row=2, column=0, padx=10, pady=(5, 10), sticky='ew')
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_frame.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(preview_frame, text='Rendered Prompt:', font=ctk.CTkFont(weight='bold')).grid(row=0, column=0, padx=10, pady=(10, 5), sticky='w')
        preview_textbox = ctk.CTkTextbox(preview_frame, font=ctk.CTkFont(family='Consolas', size=11), wrap='word', state='disabled', height=150)
        preview_textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='nsew')

        for idx, entry in enumerate(history):
            timestamp = entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            title = entry['title']
            category = entry['category']
            rendered_text = entry['rendered_text']

            item_frame = ctk.CTkFrame(list_frame)
            item_frame.grid(row=idx, column=0, padx=5, pady=5, sticky='ew')
            item_frame.grid_columnconfigure(1, weight=1)
            ctk.CTkLabel(item_frame, text=timestamp, font=ctk.CTkFont(size=11), width=150, anchor='w').grid(row=0, column=0, padx=(10, 5), pady=5, sticky='w')

            info_frame = ctk.CTkFrame(item_frame, fg_color='transparent')
            info_frame.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
            info_frame.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(info_frame, text=title, font=ctk.CTkFont(size=12, weight='bold'), anchor='w').grid(row=0, column=0, sticky='ew')
            ctk.CTkLabel(info_frame, text=f'Category: {category}', font=ctk.CTkFont(size=10), text_color='gray', anchor='w').grid(row=1, column=0, sticky='ew')

            def make_click_handler(text=rendered_text):
                def handler(event=None):
                    preview_textbox.configure(state='normal')
                    preview_textbox.delete('1.0', 'end')
                    preview_textbox.insert('1.0', text)
                    preview_textbox.configure(state='disabled')
                return handler

            handler = make_click_handler()
            item_frame.bind('<Button-1>', handler)
            info_frame.bind('<Button-1>', handler)

        if history:
            first_entry = history[0]
            preview_textbox.configure(state='normal')
            preview_textbox.delete('1.0', 'end')
            preview_textbox.insert('1.0', first_entry['rendered_text'])
            preview_textbox.configure(state='disabled')

    def on_navigate_from(self) -> None:
        super().on_navigate_from()
        self._logger.debug('Navigating from PromptsPage')

    def _show_error(self, exc: Exception) -> None:
        messagebox.showerror('Error', str(exc))