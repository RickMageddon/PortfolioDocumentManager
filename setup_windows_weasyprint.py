import os
import sys
import ctypes
from ctypes import wintypes

def setup_gtk_path():
    """Set up GTK path for WeasyPrint on Windows"""
    gtk_path = r"C:\Program Files\GTK3-Runtime Win64\bin"
    
    if os.path.exists(gtk_path):
        # Add GTK path to system PATH
        current_path = os.environ.get('PATH', '')
        if gtk_path not in current_path:
            os.environ['PATH'] = gtk_path + os.pathsep + current_path
        
        # Set additional environment variables
        os.environ['GTK_BASEPATH'] = r"C:\Program Files\GTK3-Runtime Win64"
        
        # Try to preload the GTK libraries
        try:
            # Load the libraries in the correct order
            kernel32 = ctypes.windll.kernel32
            kernel32.SetDllDirectoryW(gtk_path)
            
            # Load dependencies first
            libs_to_load = [
                'libglib-2.0-0.dll',
                'libgobject-2.0-0.dll',
                'libgio-2.0-0.dll',
                'libpango-1.0-0.dll',
                'libpangocairo-1.0-0.dll',
                'libcairo-2.dll'
            ]
            
            for lib in libs_to_load:
                lib_path = os.path.join(gtk_path, lib)
                if os.path.exists(lib_path):
                    try:
                        ctypes.CDLL(lib_path)
                        print(f"Successfully loaded {lib}")
                    except Exception as e:
                        print(f"Failed to load {lib}: {e}")
            
            return True
        except Exception as e:
            print(f"Error setting up GTK: {e}")
            return False
    else:
        print(f"GTK path not found: {gtk_path}")
        return False

if __name__ == "__main__":
    setup_gtk_path()
