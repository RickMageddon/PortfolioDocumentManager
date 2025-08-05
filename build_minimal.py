#!/usr/bin/env python3
"""
Minimal Build script for Portfolio Document Manager
Creates executable with minimal Flet dependencies to avoid Icons enum loading issues
"""

import os
import sys
import subprocess
import platform
import shutil

def install_requirements():
    """Install minimal required packages for building"""
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

def build_minimal_executable():
    """Build executable using PyInstaller with minimal dependencies"""
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
        final_name = f'PortfolioManager-{platform_name}-minimal.exe'
        windowed_flag = '--windowed'
        icon_file = 'icon.ico' if os.path.exists('icon.ico') else None
    else:
        final_name = f'PortfolioManager-{platform_name}-minimal'
        windowed_flag = '--windowed' if system == 'darwin' else '--console'
        icon_file = 'icon.png' if os.path.exists('icon.png') else None
    
    # Minimal PyInstaller command that avoids Icons enum loading
    cmd = [
        'pyinstaller',
        '--onefile',
        windowed_flag,
        '--name', 'portfolio-manager-minimal-temp',
        '--distpath', './dist',
        '--workpath', './build',
        '--specpath', './build',
        # Minimal Flet imports - avoid problematic modules
        '--hidden-import', 'flet',
        '--hidden-import', 'flet_core',
        '--hidden-import', 'flet.app',
        '--hidden-import', 'flet.core.page',
        '--hidden-import', 'flet.core.control',
        '--hidden-import', 'flet.core.colors',
        # Skip flet.core.icons to avoid enum loading issues
        '--exclude-module', 'flet.core.icons',
        # Web server dependencies
        '--hidden-import', 'websockets',
        '--hidden-import', 'uvicorn',
        '--hidden-import', 'starlette',
        '--hidden-import', 'httpx',
        # System dependencies
        '--hidden-import', 'json',
        '--hidden-import', 'datetime',
        '--hidden-import', 'os',
        '--hidden-import', 'sys',
        '--hidden-import', 'platform',
        '--noconfirm'
    ]
    
    # Add icon if available
    if icon_file:
        cmd.extend(['--icon', icon_file])
    
    # Add data files
    if os.path.exists('icon.png'):
        cmd.extend(['--add-data', f'icon.png{os.pathsep}.'])
    
    # Use minimal main script
    cmd.append('main_flet_minimal.py')
    
    print(f"Building minimal executable for {platform_name}...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("PyInstaller output:", result.stdout)
        
        # Find the generated executable
        temp_exe = None
        if system == 'windows':
            temp_exe = './dist/portfolio-manager-minimal-temp.exe'
        else:
            temp_exe = './dist/portfolio-manager-minimal-temp'
        
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
    print("=== Portfolio Document Manager Minimal Build Script ===")
    
    # Check if minimal main script exists
    if not os.path.exists('main_flet_minimal.py'):
        print("❌ main_flet_minimal.py not found!")
        return False
    
    # Install requirements
    print("Installing requirements...")
    if not install_requirements():
        print("❌ Failed to install requirements")
        return False
    
    # Create dist directory if it doesn't exist
    os.makedirs('./dist', exist_ok=True)
    
    # Build executable
    if build_minimal_executable():
        print("✅ Minimal build completed successfully!")
        return True
    else:
        print("❌ Minimal build failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
