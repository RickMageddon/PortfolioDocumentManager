#!/usr/bin/env python3
"""
Portfolio Manager Launcher - Prevents Flet installation loops
"""
import os
import sys
import subprocess
import signal

def setup_environment():
    """Setup environment to prevent Flet package installation issues"""
    # Prevent Flet from trying to auto-install packages
    os.environ['FLET_FORCE_WEB_SERVER'] = 'false'
    os.environ['FLET_VIEW'] = 'flet_app'
    os.environ['FLET_WEB_RENDERER'] = 'html'
    os.environ['FLET_OFFLINE_MODE'] = 'true'
    os.environ['FLET_SKIP_PACKAGE_INSTALL'] = 'true'
    
    # Disable pip auto-install for embedded apps
    os.environ['PIP_DISABLE_PIP_VERSION_CHECK'] = '1'
    os.environ['PIP_NO_INPUT'] = '1'

def signal_handler(signum, frame):
    """Handle interrupt signals gracefully"""
    print("\nApplication interrupted. Exiting...")
    sys.exit(0)

def main():
    """Main launcher function"""
    print("=" * 60)
    print("Portfolio Document Manager v1.5.7 - Launcher")
    print("=" * 60)
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Setup environment
    setup_environment()
    
    try:
        # Import and run the main application
        print("Loading Portfolio Manager...")
        
        # Import main_flet here to ensure environment is set first
        import main_flet
        
        # This should not loop anymore
        main_flet.main()
        
    except KeyboardInterrupt:
        print("\nApplication was interrupted by user.")
        sys.exit(0)
    except ImportError as e:
        print(f"\nERROR: Missing required packages - {e}")
        print("\nPlease install required dependencies:")
        print("pip install flet markdown weasyprint")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: Application failed to start - {e}")
        print("\nIf this error persists, please report it as a bug.")
        sys.exit(1)

if __name__ == "__main__":
    main()
