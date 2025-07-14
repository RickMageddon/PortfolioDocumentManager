#!/usr/bin/env python3
"""
Build script for Portfolio Document Manager
Creates executable files for Windows, macOS, and Linux using PyInstaller
"""

import os
import sys
import subprocess
import platform

def install_requirements():
    """Install required packages for building"""
    requirements = [
        'pyinstaller',
        'flet',
        'markdown',
        'weasyprint'
    ]
    
    for req in requirements:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', req])
        except subprocess.CalledProcessError:
            print(f"Failed to install {req}")
            return False
    return True

def build_executable():
    """Build executable using PyInstaller"""
    system = platform.system().lower()
    
    # Determine icon file
    icon_file = None
    if system == 'windows' and os.path.exists('icon.ico'):
        icon_file = 'icon.ico'
    elif os.path.exists('icon.png'):
        icon_file = 'icon.png'
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name', f'PortfolioManager-{system}',
        'main_flet.py'
    ]
    
    # Add icon if available
    if icon_file:
        cmd.insert(-1, f'--icon={icon_file}')
    
    try:
        subprocess.check_call(cmd)
        print(f"✅ Build successful for {system}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Build failed for {system}")
        return False

def main():
    print("🚀 Building Portfolio Document Manager...")
    print(f"Platform: {platform.system()} {platform.machine()}")
    
    # Install requirements
    print("\n📦 Installing build requirements...")
    if not install_requirements():
        print("❌ Failed to install requirements")
        return 1
    
    # Build executable
    print("\n🔨 Building executable...")
    if not build_executable():
        print("❌ Build failed")
        return 1
    
    print("\n✅ Build completed successfully!")
    print("📁 Executable can be found in the 'dist' folder")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
