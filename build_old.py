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
    
    # Basic PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',
        windowed_flag,
        '--name', 'portfolio-manager-temp',  # Temporary name
        '--distpath', './dist',
        '--workpath', './build',
        '--specpath', './build'
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
        'pyinstaller',
        '--onefile',
        '--name', f'PortfolioManager-{platform_name}',
        '--distpath', './dist',
        '--workpath', './build',
        '--specpath', './build'
    ]
    
    # Add platform-specific options
    if system == 'linux':
        cmd.extend([
            '--console',  # Use console for better debugging on Linux
            '--add-data', 'launch_linux.sh:.',
            '--add-data', 'portfolio-manager.desktop:.',
            '--add-data', 'icon.png:.' if os.path.exists('icon.png') else '',
            '--add-data', 'assets:assets' if os.path.exists('assets') else '',
            '--hidden-import', 'pkg_resources.py2_warn',
            '--hidden-import', 'flet.matplotlib_chart',
            '--hidden-import', 'flet.plotly_chart',
            '--collect-all', 'flet',  # Include all Flet dependencies
            '--copy-metadata', 'flet'  # Copy Flet metadata
        ])
        # Add environment variables for Linux
        os.environ['FLET_VIEW'] = 'flet_app'
        os.environ['FLET_WEB_RENDERER'] = 'html'
        
        # Try to bundle system libraries
        try:
            import subprocess
            # Check if libmpv is available and get its path
            result = subprocess.run(['ldconfig', '-p'], capture_output=True, text=True)
            if 'libmpv.so' in result.stdout:
                # Find libmpv path
                for line in result.stdout.split('\n'):
                    if 'libmpv.so' in line and '=>' in line:
                        libpath = line.split('=>')[1].strip()
                        cmd.extend(['--add-binary', f'{libpath}:.'])
                        print(f"Adding libmpv: {libpath}")
                        break
        except Exception as e:
            print(f"Warning: Could not detect libmpv: {e}")
    elif system == 'windows':
        cmd.append('--windowed')
    elif system == 'darwin':
        cmd.append('--windowed')
    
    # Add the main script
    cmd.append('main_flet.py')
    
    # Add icon if available
    if icon_file:
        cmd.insert(-2, f'--icon={icon_file}')
    
    try:
        subprocess.check_call(cmd)
        
        # Post-build steps for Linux
        if system == 'linux':
            post_build_linux(platform_name)
        
        print(f"✅ Build successful for {platform_name}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Build failed for {platform_name}")
        return False

def post_build_linux(platform_name):
    """Post-build steps for Linux"""
    try:
        dist_dir = './dist'
        executable_path = os.path.join(dist_dir, f'PortfolioManager-{platform_name}')
        launcher_script = os.path.join(dist_dir, 'launch_linux.sh')
        
        # Copy launcher script to dist directory
        if os.path.exists('launch_linux.sh'):
            subprocess.check_call(['cp', 'launch_linux.sh', launcher_script])
            subprocess.check_call(['chmod', '+x', launcher_script])
            print("✅ Launcher script copied and made executable")
        
        # Copy desktop file
        desktop_file = os.path.join(dist_dir, 'portfolio-manager.desktop')
        if os.path.exists('portfolio-manager.desktop'):
            subprocess.check_call(['cp', 'portfolio-manager.desktop', desktop_file])
            print("✅ Desktop file copied")
        
        # Make executable file executable
        if os.path.exists(executable_path):
            subprocess.check_call(['chmod', '+x', executable_path])
            print("✅ Main executable made executable")
        
        # Create installation instructions
        install_instructions = os.path.join(dist_dir, 'INSTALL_LINUX.md')
        with open(install_instructions, 'w') as f:
            f.write(f"""# Portfolio Document Manager - Linux Installation

## Quick Start
1. Make sure the executable is executable: `chmod +x PortfolioManager-{platform_name}`
2. Run the launcher script: `./launch_linux.sh`

## Alternative Start Methods
- Direct execution: `./PortfolioManager-{platform_name}`
- With logging: `./PortfolioManager-{platform_name} 2>&1 | tee app.log`

## Desktop Integration
1. Copy `portfolio-manager.desktop` to `~/.local/share/applications/`
2. Update the Exec path in the .desktop file to point to the correct location
3. Run: `update-desktop-database ~/.local/share/applications/`

## Troubleshooting
- Check `~/.portfolio_manager.log` for error messages
- Make sure you have a working X11 or Wayland display
- Try running with `DISPLAY=:0 ./PortfolioManager-{platform_name}`

## Dependencies
The application is built as a standalone executable and should not require additional Python packages.
If you encounter issues, make sure your system has basic GUI libraries installed:
- On Ubuntu/Debian: `sudo apt install libgtk-3-0 libglib2.0-0`
- On CentOS/RHEL: `sudo yum install gtk3 glib2`
""")
        print("✅ Installation instructions created")
        
    except Exception as e:
        print(f"⚠️  Post-build steps failed: {e}")
        # Don't fail the build for post-build issues

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
