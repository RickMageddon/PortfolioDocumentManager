#!/usr/bin/env python3
"""
PyInstaller hook for Flet framework
This hook helps PyInstaller correctly bundle Flet applications by:
1. Including only essential Flet modules
2. Excluding problematic large modules like the full Icons enum
3. Adding required data files
"""

from PyInstaller.utils.hooks import collect_all, collect_submodules

# Collect core Flet modules
datas, binaries, hiddenimports = collect_all('flet_core')

# Add essential flet modules
hiddenimports += [
    'flet',
    'flet.app',
    'flet.core.page',
    'flet.core.control',
    'flet.core.colors',
    'flet.core.text_style', 
    'flet.core.border',
    'flet.core.box',
    'flet.core.badge',
    'flet.core.adaptive_control',
    'flet.fastapi',
    'flet.utils',
    # Web server dependencies
    'websockets',
    'websockets.server',
    'uvicorn',
    'uvicorn.main',
    'starlette',
    'httpx',
    # System modules
    'asyncio',
    'threading',
    'json',
    'datetime',
    'typing',
    'pathlib'
]

# Exclude problematic modules that cause issues with PyInstaller
excludedimports = [
    'flet.core.icons'  # This huge enum causes problems
]
