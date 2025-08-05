#!/usr/bin/env python3
"""
Build script for Portfolio Document Manager
Creates executable files for Windows, macOS, and Linux using PyInstaller
"""

import os
import sys
import subprocess
import platform
import shutil

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
    
    # Map platform names to match GitHub Actions matrix
    platform_mapping = {
        'windows': 'windows',
        'darwin': 'darwin', 
        'linux': 'linux'
    }
    
    platform_name = platform_mapping.get(system, system)
    
    # Determine final executable name with extension
    if system == 'windows':
        final_name = f'PortfolioManager-{platform_name}.exe'
        windowed_flag = '--windowed'
        icon_file = 'icon.ico' if os.path.exists('icon.ico') else None
    else:
        final_name = f'PortfolioManager-{platform_name}'
        windowed_flag = '--windowed' if system == 'darwin' else '--console'
        icon_file = 'icon.png' if os.path.exists('icon.png') else None
    
    # Enhanced PyInstaller command with comprehensive Flet dependencies
    cmd = [
        'pyinstaller',
        '--onefile',
        windowed_flag,
        '--name', 'portfolio-manager-temp',  # Temporary name
        '--distpath', './dist',
        '--workpath', './build',
        '--specpath', './build',
        # Collect all Flet related packages
        '--collect-all', 'flet',
        '--collect-all', 'flet_core',
        '--collect-all', 'flet_runtime',
        '--collect-submodules', 'flet',
        '--collect-submodules', 'flet_core',
        # Hidden imports for all Flet components
        '--hidden-import', 'flet',
        '--hidden-import', 'flet_core',
        '--hidden-import', 'flet_runtime',
        '--hidden-import', 'flet.app',
        '--hidden-import', 'flet.core',
        '--hidden-import', 'flet.core.page',
        '--hidden-import', 'flet.core.control',
        '--hidden-import', 'flet.core.icons',
        '--hidden-import', 'flet.core.types',
        '--hidden-import', 'flet.core.colors',
        '--hidden-import', 'flet.core.text_style',
        '--hidden-import', 'flet.core.border',
        '--hidden-import', 'flet.core.box',
        '--hidden-import', 'flet.core.badge',
        '--hidden-import', 'flet.core.adaptive_control',
        '--hidden-import', 'flet.fastapi',
        '--hidden-import', 'flet.utils',
        # Web server dependencies
        '--hidden-import', 'websockets',
        '--hidden-import', 'websockets.server',
        '--hidden-import', 'websockets.client',
        '--hidden-import', 'uvicorn',
        '--hidden-import', 'uvicorn.main',
        '--hidden-import', 'uvicorn.server',
        '--hidden-import', 'starlette',
        '--hidden-import', 'starlette.applications',
        '--hidden-import', 'starlette.routing',
        '--hidden-import', 'httpx',
        '--hidden-import', 'httpx._client',
        # Additional system dependencies
        '--hidden-import', 'asyncio',
        '--hidden-import', 'threading',
        '--hidden-import', 'json',
        '--hidden-import', 'datetime',
        '--hidden-import', 'enum',
        '--hidden-import', 'typing',
        '--hidden-import', 'pathlib',
        '--hidden-import', 'os',
        '--hidden-import', 'sys',
        '--hidden-import', 'platform',
        '--noconfirm'  # Don't ask for confirmation
    ]
    
    # Add icon if available
    if icon_file:
        cmd.extend(['--icon', icon_file])
    
    # Add data files
    if os.path.exists('icon.png'):
        cmd.extend(['--add-data', f'icon.png{os.pathsep}.'])
    
    # Add main script
    cmd.append('main_flet.py')
    
    print(f"Building executable for {platform_name}...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("PyInstaller output:", result.stdout)
        
        # Find the generated executable
        temp_exe = None
        if system == 'windows':
            temp_exe = './dist/portfolio-manager-temp.exe'
        else:
            temp_exe = './dist/portfolio-manager-temp'
        
        # Check if temporary executable exists
        if os.path.exists(temp_exe):
            # Rename to final name
            final_path = f'./dist/{final_name}'
            shutil.move(temp_exe, final_path)
            print(f"✅ Successfully built: {final_path}")
            
            # Verify the file exists
            if os.path.exists(final_path):
                size = os.path.getsize(final_path)
                print(f"✅ File size: {size} bytes")
                return True
            else:
                print(f"❌ Final file not found: {final_path}")
                return False
        else:
            print(f"❌ Temporary executable not found: {temp_exe}")
            # List all files in dist directory
            if os.path.exists('./dist'):
                print("Files in dist directory:")
                for f in os.listdir('./dist'):
                    print(f"  - {f}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller failed: {e}")
        print(f"Stderr: {e.stderr}")
        return False

def main():
    """Main build function"""
    print("=== Portfolio Document Manager Build Script ===")
    
    # Check if main_flet.py exists
    if not os.path.exists('main_flet.py'):
        print("❌ main_flet.py not found!")
        return False
    
    # Install requirements
    print("Installing requirements...")
    if not install_requirements():
        print("❌ Failed to install requirements")
        return False
    
    # Create dist directory if it doesn't exist
    os.makedirs('./dist', exist_ok=True)
    
    # Build executable
    if build_executable():
        print("✅ Build completed successfully!")
        return True
    else:
        print("❌ Build failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
