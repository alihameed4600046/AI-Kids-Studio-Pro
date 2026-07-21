"""
Create Project Dialog Module

This module provides the CreateProjectDialog class for creating new projects
through a modal dialog interface.
"""

import customtkinter as ctk


class CreateProjectDialog(ctk.CTkToplevel):
    """
    A modal dialog for creating new projects.
    
    This dialog provides a form for entering project details including
    name, description, category, and project location.
    """
    
    def __init__(self, master, **kwargs) -> None:
        """
        Initialize the CreateProjectDialog.
        
        Args:
            master: The parent CTk window.
            **kwargs: Additional keyword arguments passed to CTkToplevel.
        """
        super().__init__(master, **kwargs)
        
        self._setup_window()
        self._create_widgets()
        self._setup_layout()
    
    def _setup_window(self) -> None:
        """Configure the dialog window properties."""
        self.title("Create Project")
        self.geometry("500x420")
        self.resizable(False, False)
    
    def _create_widgets(self) -> None:
        """Create all dialog widgets."""
        # Main container
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        
        # Title label
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Create Project",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        
        # Form frame
        self.form_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        # Project Name field
        self.name_label = ctk.CTkLabel(
            self.form_frame,
            text="Project Name",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        self.name_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Enter project name",
            height=35,
            font=ctk.CTkFont(size=13)
        )
        
        # Description field
        self.description_label = ctk.CTkLabel(
            self.form_frame,
            text="Description",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        self.description_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Enter description",
            height=35,
            font=ctk.CTkFont(size=13)
        )
        
        # Category field
        self.category_label = ctk.CTkLabel(
            self.form_frame,
            text="Category",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        self.category_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Enter category",
            height=35,
            font=ctk.CTkFont(size=13)
        )
        
        # Project Location field
        self.location_label = ctk.CTkLabel(
            self.form_frame,
            text="Project Location",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        self.location_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Enter project location",
            height=35,
            font=ctk.CTkFont(size=13)
        )
        
        # Error label (inline validation feedback)
        self.error_label = ctk.CTkLabel(
            self.form_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="red",
            anchor="w"
        )
        
        # Button frame
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.cancel_button = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            width=100,
            height=35,
            font=ctk.CTkFont(size=13),
            fg_color="gray",
            hover_color="gray50"
        )
        self.create_button = ctk.CTkButton(
            self.button_frame,
            text="Create",
            width=100,
            height=35,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._on_create
        )
    
    def _setup_layout(self) -> None:
        """Arrange widgets using grid layout."""
        # Main frame
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Title
        self.title_label.grid(row=0, column=0, sticky="w", pady=(0, 20))
        
        # Form frame
        self.form_frame.grid(row=1, column=0, sticky="ew")
        self.form_frame.grid_columnconfigure(0, weight=1)
        
        # Form fields
        row = 0
        # Project Name
        self.name_label.grid(row=row, column=0, sticky="ew", pady=(0, 5))
        row += 1
        self.name_entry.grid(row=row, column=0, sticky="ew", pady=(0, 15))
        row += 1
        
        # Description
        self.description_label.grid(row=row, column=0, sticky="ew", pady=(0, 5))
        row += 1
        self.description_entry.grid(row=row, column=0, sticky="ew", pady=(0, 15))
        row += 1
        
        # Category
        self.category_label.grid(row=row, column=0, sticky="ew", pady=(0, 5))
        row += 1
        self.category_entry.grid(row=row, column=0, sticky="ew", pady=(0, 15))
        row += 1
        
        # Project Location
        self.location_label.grid(row=row, column=0, sticky="ew", pady=(0, 5))
        row += 1
        self.location_entry.grid(row=row, column=0, sticky="ew", pady=(0, 15))
        row += 1
        
        # Error label (inline validation feedback)
        self.error_label.grid(row=row, column=0, sticky="ew", pady=(0, 15))
        row += 1
        
        # Button frame
        self.button_frame.grid(row=2, column=0, sticky="ew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.cancel_button.grid(row=0, column=1, padx=(10, 0))
        self.create_button.grid(row=0, column=2)
    
    def _validate_inputs(self) -> bool:
        """
        Validate required input fields.
        
        Returns:
            True if all required fields are valid, False otherwise.
        """
        name = self.name_entry.get().strip()
        location = self.location_entry.get().strip()
        
        if not name:
            self.error_label.configure(text="Project Name is required")
            return False
        
        if not location:
            self.error_label.configure(text="Project Location is required")
            return False
        
        # Clear error on success
        self.error_label.configure(text="")
        return True
    
    def _on_create(self) -> None:
        """Handle Create button click with validation."""
        if not self._validate_inputs():
            return
        # Validation passed - no further action (placeholder for future logic)


__all__ = ["CreateProjectDialog"]
