#!/usr/bin/env python3
"""
Release script for Portfolio Document Manager
Prepares the project for GitHub release
"""

import os
import sys
import subprocess
import shutil
import zipfile
from pathlib import Path

def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Cleaned {dir_name}/")

def create_executable():
    """Create platform-specific executable"""
    import platform
    
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # Determine platform name
    if system == 'darwin':
        platform_name = 'macos'
    elif system == 'windows':
        platform_name = 'windows'
    else:
        platform_name = 'linux'
    
    # Architecture
    if machine in ['x86_64', 'amd64']:
        arch = 'x64'
    elif machine in ['aarch64', 'arm64']:
        arch = 'arm64'
    else:
        arch = machine
    
    exe_name = f'PortfolioManager-{platform_name}-{arch}'
    if system == 'windows':
        exe_name += '.exe'
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name', exe_name,
        '--clean',
        '--noconfirm',
        'main.py'
    ]
    
    print(f"🔨 Building {exe_name}...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Successfully built {exe_name}")
            return True, exe_name
        else:
            print(f"❌ Build failed: {result.stderr}")
            return False, None
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False, None

def create_release_package():
    """Create release package with documentation"""
    release_dir = Path('release')
    release_dir.mkdir(exist_ok=True)
    
    # Copy documentation files
    docs_to_include = [
        'README.md',
        'LICENSE',
        'CHANGELOG.md',
        'requirements.txt'
    ]
    
    for doc in docs_to_include:
        if os.path.exists(doc):
            shutil.copy2(doc, release_dir / doc)
            print(f"📄 Added {doc} to release package")
    
    # Copy executable from dist
    dist_dir = Path('dist')
    if dist_dir.exists():
        for exe_file in dist_dir.glob('PortfolioManager*'):
            shutil.copy2(exe_file, release_dir / exe_file.name)
            print(f"🎯 Added {exe_file.name} to release package")
    
    return release_dir

def create_zip_archive(release_dir):
    """Create ZIP archive for distribution"""
    import platform
    
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == 'darwin':
        platform_name = 'macos'
    elif system == 'windows':
        platform_name = 'windows'
    else:
        platform_name = 'linux'
    
    if machine in ['x86_64', 'amd64']:
        arch = 'x64'
    elif machine in ['aarch64', 'arm64']:
        arch = 'arm64'
    else:
        arch = machine
    
    zip_name = f'PortfolioManager-v1.0.0-{platform_name}-{arch}.zip'
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in release_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(release_dir)
                zipf.write(file_path, arcname)
        
    print(f"📦 Created {zip_name}")
    return zip_name

def main():
    print("🚀 Preparing Portfolio Document Manager for release...")
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("❌ main.py not found. Run this script from the project root.")
        return 1
    
    # Clean previous builds
    print("\n🧹 Cleaning previous builds...")
    clean_build_dirs()
    
    # Install requirements
    print("\n📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Requirements installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return 1
    
    # Create executable
    print("\n🔨 Building executable...")
    success, exe_name = create_executable()
    if not success:
        print("❌ Failed to create executable")
        return 1
    
    # Create release package
    print("\n📦 Creating release package...")
    release_dir = create_release_package()
    
    # Create ZIP archive
    print("\n🗜️ Creating ZIP archive...")
    zip_file = create_zip_archive(release_dir)
    
    print(f"\n✅ Release preparation complete!")
    print(f"📁 Release files:")
    print(f"   - {zip_file}")
    print(f"   - release/ directory with all files")
    print(f"\n🎯 Ready to upload to GitHub!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
