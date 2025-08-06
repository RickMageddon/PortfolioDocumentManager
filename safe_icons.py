#!/usr/bin/env python3
"""
Safe icons module for Portfolio Manager
This module defines only the icons we actually use to avoid the PyInstaller enum issue
"""

class SafeIcons:
    """Safe icons class with only the icons we need"""
    # Menu and navigation
    MENU = "menu"
    LANGUAGE = "language"
    LIGHT_MODE = "light_mode"
    DARK_MODE = "dark_mode"
    ARROW_BACK = "arrow_back"
    
    # Actions
    ADD = "add"
    SAVE = "save"
    EDIT = "edit"
    DELETE = "delete"
    
    # Content
    FEEDBACK = "feedback"
    FEEDBACK_OUTLINED = "feedback_outlined"
    LIST_ALT = "list_alt"
    UPLOAD_FILE = "upload_file"
    DESCRIPTION = "description"
    
    # Status
    INFO = "info"
    WARNING = "warning"
    CHECK_CIRCLE = "check_circle"

# Export as Icons for compatibility
Icons = SafeIcons
