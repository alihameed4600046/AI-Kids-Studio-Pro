"""Navigation framework for AI Kids Studio Pro.

This module re-exports the navigation classes from their canonical locations.
"""

from src.navigation.navigation_manager import NavigationManager
from src.views.pages.base_page import BasePage
from src.views.pages.home_page import HomePage


__all__ = ["NavigationManager", "BasePage", "HomePage"]