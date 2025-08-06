#!/usr/bin/env python3
"""
Portfolio Document Manager - Safe Icons Version
A modern desktop application for managing TI portfolio documents with Linux compatibility
"""

import flet as ft
import json
import datetime
import os
import sys
import platform

# Import our safe icons instead of the problematic flet.core.icons
try:
    from safe_icons import Icons
except ImportError:
    # Fallback to strings if safe_icons is not available
    class Icons:
        MENU = "menu"
        LANGUAGE = "language" 
        LIGHT_MODE = "light_mode"
        DARK_MODE = "dark_mode"
        ARROW_BACK = "arrow_back"
        ADD = "add"
        SAVE = "save"
        EDIT = "edit"
        DELETE = "delete"
        FEEDBACK = "feedback"
        FEEDBACK_OUTLINED = "feedback_outlined"
        LIST_ALT = "list_alt"
        UPLOAD_FILE = "upload_file"
        DESCRIPTION = "description"
        INFO = "info"
        WARNING = "warning"
        CHECK_CIRCLE = "check_circle"

def main(page: ft.Page):
    """Main application entry point"""
    try:
        # Basic page setup
        page.title = "Portfolio Document Manager - TI (Safe Version)"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window_width = 1200
        page.window_height = 800
        
        # Simple test interface to verify Flet works
        def test_button_click(e):
            test_text.value = "✅ Flet framework is working!"
            page.update()
            
        test_text = ft.Text("Testing Flet framework compatibility...", size=16)
        test_button = ft.ElevatedButton(
            "Test Flet",
            icon=Icons.CHECK_CIRCLE,
            on_click=test_button_click
        )
        
        # Add content to page
        page.add(
            ft.Column([
                ft.Text("Portfolio Document Manager", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Safe Icons Version - Linux Compatible", size=16),
                ft.Divider(),
                test_text,
                test_button,
                ft.Text(f"Platform: {platform.system()} {platform.release()}", size=12),
                ft.Text(f"Python: {sys.version}", size=12)
            ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        
        print("✅ Application initialized successfully")
        
    except Exception as e:
        print(f"❌ Error initializing application: {e}")
        # Show error on page if possible
        try:
            page.add(ft.Text(f"Error: {str(e)}", color=ft.Colors.RED))
        except:
            pass

if __name__ == "__main__":
    print("==" * 25)
    print("Portfolio Document Manager - Safe Version")  
    print("==" * 25)
    print(f"Running on {platform.system()} {platform.release()}")
    print(f"Python {sys.version}")
    
    if "DISPLAY" in os.environ:
        print(f"DISPLAY is set to: {os.environ['DISPLAY']}")
    
    session_type = os.environ.get("XDG_SESSION_TYPE", "unknown")
    print(f"Session type: {session_type}")
    
    print("Starting safe Flet application...")
    
    try:
        # Use Flet app with minimal configuration
        ft.app(target=main, view=ft.AppView.FLET_APP)
        print("✅ Application started successfully")
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        print("This is a known issue with Flet framework bundling")
        sys.exit(1)
