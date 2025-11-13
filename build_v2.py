"""
MediaVault Scanner v2.0 - Build Script
Creates a deployable Windows executable using PyInstaller

This script:
1. Validates the environment
2. Cleans previous builds
3. Runs PyInstaller with the spec file
4. Verifies the build
5. Reports build statistics
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def print_step(step_num, text):
    """Print a formatted step"""
    print(f"\n[Step {step_num}] {text}")
    print("-" * 70)

def check_dependencies():
    """Check if required dependencies are installed"""
    print_step(1, "Checking Dependencies")
    
    required = {
        'PyInstaller': 'PyInstaller',
        'customtkinter': 'customtkinter',
        'PIL': 'Pillow',
        'cv2': 'opencv-python',
        'pytesseract': 'pytesseract',
        'exifread': 'exifread',
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - MISSING")
            missing.append(package)
    
    # Check optional dependencies
    print("\nOptional Dependencies (for Deepseek-VL):")
    optional = ['torch', 'transformers', 'accelerate', 'sentencepiece']
    for module in optional:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError:
            print(f"  ○ {module} - Not installed (lightweight build)")
    
    if missing:
        print(f"\n❌ ERROR: Missing required dependencies: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False
    
    print("\n✅ All required dependencies installed")
    return True

def clean_build_dirs():
    """Remove previous build artifacts"""
    print_step(2, "Cleaning Previous Builds")
    
    dirs_to_clean = ['build', 'dist']
    files_to_clean = ['MediaVaultScanner.spec']  # Old spec file if exists
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"  Removing {dir_name}/")
            shutil.rmtree(dir_name)
    
    for file_name in files_to_clean:
        if os.path.exists(file_name) and file_name != 'mediavault.spec':
            print(f"  Removing {file_name}")
            os.remove(file_name)
    
    print("✅ Build directories cleaned")

def run_pyinstaller():
    """Run PyInstaller with the spec file"""
    print_step(3, "Running PyInstaller")
    
    spec_file = 'mediavault.spec'
    if not os.path.exists(spec_file):
        print(f"❌ ERROR: {spec_file} not found")
        return False
    
    print(f"  Using spec file: {spec_file}")
    print("  Building executable (this may take several minutes)...\n")
    
    try:
        result = subprocess.run(
            ['pyinstaller', '--clean', spec_file],
            check=True,
            capture_output=False,
            text=True
        )
        print("\n✅ PyInstaller completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ ERROR: PyInstaller failed with return code {e.returncode}")
        return False
    except FileNotFoundError:
        print("❌ ERROR: PyInstaller not found. Install with: pip install pyinstaller")
        return False

def verify_build():
    """Verify the build was successful"""
    print_step(4, "Verifying Build")
    
    exe_path = Path('dist/MediaVaultScanner.exe')
    
    if not exe_path.exists():
        print("❌ ERROR: Executable not found at dist/MediaVaultScanner.exe")
        return False
    
    # Get file size
    size_bytes = exe_path.stat().st_size
    size_mb = size_bytes / (1024 * 1024)
    
    print(f"  ✓ Executable found: {exe_path}")
    print(f"  ✓ File size: {size_mb:.2f} MB ({size_bytes:,} bytes)")
    
    # Check if it's a reasonable size
    if size_mb < 10:
        print("  ⚠ Warning: Executable seems unusually small")
    elif size_mb > 500:
        print("  ⚠ Warning: Executable seems unusually large")
    
    print("\n✅ Build verification passed")
    return True

def print_summary():
    """Print build summary and next steps"""
    print_header("Build Complete!")
    
    print("📦 Deployment Package:")
    print(f"   Location: dist/MediaVaultScanner.exe")
    
    exe_path = Path('dist/MediaVaultScanner.exe')
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"   Size: {size_mb:.2f} MB")
    
    print("\n📋 Next Steps:")
    print("   1. Test the executable: dist\\MediaVaultScanner.exe")
    print("   2. Distribute with installation instructions")
    print("   3. Users must install Tesseract OCR separately")
    print("   4. Optional: Users can install PyTorch for Deepseek-VL support")
    
    print("\n📚 Documentation:")
    print("   - README.md - Main documentation")
    print("   - QUICKSTART_VL_OCR.md - Quick start guide")
    print("   - VL_OCR_DEPLOYMENT_GUIDE.md - Deployment guide")
    
    print("\n🎉 MediaVault Scanner v2.0 is ready for deployment!")

def main():
    """Main build process"""
    print_header("MediaVault Scanner v2.0 - Build Process")
    
    # Step 1: Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Step 2: Clean previous builds
    clean_build_dirs()
    
    # Step 3: Run PyInstaller
    if not run_pyinstaller():
        sys.exit(1)
    
    # Step 4: Verify build
    if not verify_build():
        sys.exit(1)
    
    # Print summary
    print_summary()

if __name__ == '__main__':
    main()

