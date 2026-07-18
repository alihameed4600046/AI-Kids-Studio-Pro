"""Navigation package for AI Kids Studio Pro.

This package provides the NavigationManager for managing page navigation,
page registration, page switching, and page lifecycle hooks.
"""

from src.navigation.navigation_manager import NavigationManager
from src.views.pages.base_page import BasePage

__all__ = ["NavigationManager", "BasePage"]
