"""
MediaVault Scanner - Build Script
Automates the process of building the Windows executable using PyInstaller.

Usage:
    python build.py
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def print_header(message):
    """Print a formatted header message."""
    print("\n" + "=" * 70)
    print(f"  {message}")
    print("=" * 70 + "\n")


def check_requirements():
    """Check if all required packages are installed."""
    print_header("Checking Requirements")
    
    required_packages = {
        'customtkinter': 'customtkinter',
        'Pillow': 'PIL',
        'exifread': 'exifread',
        'pytesseract': 'pytesseract',
        'opencv-python': 'cv2',
        'numpy': 'numpy',
        'pyinstaller': 'PyInstaller'
    }

    missing_packages = []

    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"✓ {package_name} is installed")
        except ImportError:
            print(f"✗ {package_name} is NOT installed")
            missing_packages.append(package_name)
    
    if missing_packages:
        print("\n⚠️  Missing packages detected!")
        print("Please install them using:")
        print(f"    pip install {' '.join(missing_packages)}")
        return False
    
    print("\n✓ All required packages are installed!")
    return True


def clean_build_directories():
    """Clean previous build artifacts."""
    print_header("Cleaning Build Directories")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Removing {dir_name}/")
            shutil.rmtree(dir_name)
    
    # Clean .spec backup files
    for spec_file in Path('.').glob('*.spec.bak'):
        print(f"Removing {spec_file}")
        spec_file.unlink()
    
    print("✓ Build directories cleaned!")


def build_executable():
    """Build the executable using PyInstaller."""
    print_header("Building Executable")
    
    if not os.path.exists('mediavault.spec'):
        print("✗ mediavault.spec not found!")
        print("Please ensure mediavault.spec exists in the current directory.")
        return False
    
    print("Running PyInstaller...")
    print("This may take several minutes...\n")
    
    try:
        result = subprocess.run(
            ['pyinstaller', 'mediavault.spec'],
            check=True,
            capture_output=False
        )
        
        print("\n✓ Build completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed with error code {e.returncode}")
        return False
    except FileNotFoundError:
        print("\n✗ PyInstaller not found!")
        print("Please install it using: pip install pyinstaller")
        return False


def verify_executable():
    """Verify that the executable was created."""
    print_header("Verifying Build")
    
    exe_path = Path('dist') / 'MediaVaultScanner.exe'
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✓ Executable created successfully!")
        print(f"  Location: {exe_path.absolute()}")
        print(f"  Size: {size_mb:.2f} MB")
        return True
    else:
        print("✗ Executable not found in dist/ directory")
        return False


def print_next_steps():
    """Print instructions for next steps."""
    print_header("Next Steps")
    
    print("Your executable is ready! Here's what to do next:\n")
    print("1. Test the executable:")
    print("   - Navigate to the dist/ folder")
    print("   - Run MediaVaultScanner.exe")
    print("   - Test all features\n")
    print("2. Distribute the application:")
    print("   - Copy MediaVaultScanner.exe to your target location")
    print("   - Include README.md and QUICKSTART.md")
    print("   - Remind users to install Tesseract OCR\n")
    print("3. Important Notes:")
    print("   - Tesseract is NOT bundled with the executable")
    print("   - Users must install Tesseract separately")
    print("   - See README.md for Tesseract installation instructions\n")
    print("📦 Build complete! Happy distributing!")


def main():
    """Main build process."""
    print_header("MediaVault Scanner - Build Script")
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Clean previous builds
    clean_build_directories()
    
    # Build executable
    if not build_executable():
        print("\n❌ Build process failed!")
        sys.exit(1)
    
    # Verify build
    if not verify_executable():
        print("\n❌ Build verification failed!")
        sys.exit(1)
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    main()

