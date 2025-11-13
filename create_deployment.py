"""
MediaVault Scanner v2.0 - Complete Deployment Package Creator
Creates a ready-to-distribute deployment package with all necessary files

This script:
1. Validates the environment
2. Cleans previous builds
3. Runs PyInstaller to build the executable
4. Creates a deployment folder with all necessary files
5. Generates installation instructions
6. Creates a ZIP archive for distribution
"""

import os
import sys
import shutil
import subprocess
import zipfile
from pathlib import Path
from datetime import datetime

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")

def print_step(step_num, text):
    """Print a formatted step"""
    print(f"\n[Step {step_num}] {text}")
    print("-" * 80)

def check_dependencies():
    """Check if required dependencies are installed"""
    print_step(1, "Checking Dependencies")
    
    required = {
        'PyInstaller': 'pyinstaller',
        'customtkinter': 'customtkinter',
        'PIL': 'Pillow',
        'cv2': 'opencv-python',
        'pytesseract': 'pytesseract',
        'exifread': 'exifread',
        'llama_cpp': 'llama-cpp-python',
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n❌ ERROR: Missing required dependencies: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False
    
    print("\n✅ All required dependencies installed")
    return True

def clean_build_dirs():
    """Remove previous build artifacts"""
    print_step(2, "Cleaning Previous Builds")
    
    dirs_to_clean = ['build', 'dist', 'deployment_package']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"  Removing {dir_name}/")
            shutil.rmtree(dir_name)
    
    print("✅ Build directories cleaned")

def run_pyinstaller():
    """Run PyInstaller with the spec file"""
    print_step(3, "Building Executable with PyInstaller")
    
    spec_file = 'mediavault.spec'
    if not os.path.exists(spec_file):
        print(f"❌ ERROR: {spec_file} not found")
        return False
    
    print(f"  Using spec file: {spec_file}")
    print("  Building executable (this may take 5-10 minutes)...\n")
    
    try:
        subprocess.run(
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
    
    print("\n✅ Build verification passed")
    return True

def create_deployment_package():
    """Create a complete deployment package"""
    print_step(5, "Creating Deployment Package")
    
    # Create deployment folder
    timestamp = datetime.now().strftime("%Y%m%d")
    deploy_dir = Path(f"deployment_package/MediaVaultScanner_v2.0_{timestamp}")
    deploy_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"  Creating package at: {deploy_dir}")
    
    # Copy executable
    print("  Copying executable...")
    shutil.copy('dist/MediaVaultScanner.exe', deploy_dir / 'MediaVaultScanner.exe')
    
    # Copy documentation
    print("  Copying documentation...")
    docs_to_copy = [
        'README.md',
        'LICENSE',
        'IMPLEMENTATION_COMPLETE.md',
    ]
    
    for doc in docs_to_copy:
        if os.path.exists(doc):
            shutil.copy(doc, deploy_dir / doc)
    
    # Copy scripts folder
    print("  Copying scripts...")
    if os.path.exists('scripts'):
        shutil.copytree('scripts', deploy_dir / 'scripts', dirs_exist_ok=True)

    # Create models folder (empty, for user to place GGUF model)
    print("  Creating models folder...")
    models_dir = deploy_dir / 'models'
    models_dir.mkdir(exist_ok=True)

    # Create a README in models folder
    with open(models_dir / 'README.txt', 'w') as f:
        f.write("""MediaVault Scanner - GGUF Model Folder
========================================

This folder should contain the Deepseek GGUF model file.

REQUIRED FILE:
--------------
deepseek-ocr.gguf  (2-7GB depending on quantization level)

DOWNLOAD INSTRUCTIONS:
----------------------
1. Download the Deepseek GGUF model file from your model source
2. Place it in this folder as: deepseek-ocr.gguf
3. Use the download script: ..\scripts\download_model.ps1

ALTERNATIVE:
------------
If you don't have the GGUF model, the application will automatically
fall back to Tesseract OCR (which you must install separately).

For more information, see README.md in the parent folder.
""")

    # Create installation instructions
    print("  Creating installation instructions...")
    create_install_instructions(deploy_dir)

    print(f"\n✅ Deployment package created at: {deploy_dir}")
    return deploy_dir

def create_install_instructions(deploy_dir):
    """Create detailed installation instructions"""

    instructions = """MediaVault Scanner v2.0 - Installation Instructions
======================================================

Thank you for downloading MediaVault Scanner!

QUICK START (3 Steps):
======================

Step 1: Install Tesseract OCR (REQUIRED)
-----------------------------------------
1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer: tesseract-ocr-w64-setup-*.exe
3. Add to Windows PATH (recommended) or configure path in the app

Step 2: (OPTIONAL) Download GGUF Model for High-Performance OCR
----------------------------------------------------------------
1. Download the Deepseek GGUF model file (~2-7GB)
2. Place it in the 'models' folder as: deepseek-ocr.gguf
3. Or use the download script: scripts\\download_model.ps1

Step 3: Run the Application
----------------------------
1. Double-click MediaVaultScanner.exe
2. Complete the setup wizard on first run
3. Select a folder to scan and click "Start Scan"

ADVANCED: GPU Acceleration (Optional)
======================================

For high-performance OCR with GPU acceleration, you need llama-cpp-python
with GPU support. This is OPTIONAL - the app works without it.

For NVIDIA GPUs (CUDA):
-----------------------
1. Install CUDA Toolkit 11.8+ from: https://developer.nvidia.com/cuda-downloads
2. Open PowerShell and run:
   $env:FORCE_CMAKE=1
   $env:CMAKE_ARGS="-DLLAMA_CUBLAS=on"
   pip install llama-cpp-python --no-cache-dir

For AMD GPUs (ROCm/HIP):
------------------------
1. Install AMD ROCm from: https://rocm.docs.amd.com/
2. Open PowerShell and run:
   $env:FORCE_CMAKE=1
   $env:CMAKE_ARGS="-DLLAMA_HIP=on"
   pip install llama-cpp-python --no-cache-dir

SYSTEM REQUIREMENTS:
====================

Minimum (Tesseract Only):
- Windows 10/11 (64-bit)
- 4GB RAM
- 500MB disk space
- Tesseract OCR installed

Recommended (GGUF OCR):
- Windows 10/11 (64-bit)
- 8GB RAM (16GB recommended)
- 10GB disk space
- NVIDIA GPU with 4GB+ VRAM OR AMD GPU with ROCm support
- CUDA 11.8+ or ROCm 5.0+

TROUBLESHOOTING:
================

Problem: "Tesseract not found"
Solution: Install Tesseract and add to PATH, or configure path in setup dialog

Problem: "GGUF model not found"
Solution: Download the model and place in models/deepseek-ocr.gguf

Problem: Application falls back to Tesseract
Solution: This is normal if GGUF model is not available. Install the model for better OCR.

Problem: GPU not detected
Solution: Install CUDA/ROCm drivers and rebuild llama-cpp-python with GPU support

SUPPORT:
========

For more information, see README.md
For issues, visit: https://github.com/takkekatechie/MediaVault

Enjoy using MediaVault Scanner!
"""

    with open(deploy_dir / 'INSTALL.txt', 'w') as f:
        f.write(instructions)

def create_zip_archive(deploy_dir):
    """Create a ZIP archive of the deployment package"""
    print_step(6, "Creating ZIP Archive")

    zip_path = Path(f"{deploy_dir}.zip")

    print(f"  Creating archive: {zip_path}")
    print("  Compressing files...")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(deploy_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(deploy_dir.parent)
                zipf.write(file_path, arcname)
                print(f"    Added: {arcname}")

    # Get ZIP size
    zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"\n  ✓ Archive created: {zip_path}")
    print(f"  ✓ Archive size: {zip_size_mb:.2f} MB")

    print("\n✅ ZIP archive created successfully")
    return zip_path

def print_summary(deploy_dir, zip_path):
    """Print deployment summary"""
    print_header("Deployment Package Complete!")

    exe_path = deploy_dir / 'MediaVaultScanner.exe'
    exe_size_mb = exe_path.stat().st_size / (1024 * 1024)
    zip_size_mb = zip_path.stat().st_size / (1024 * 1024)

    print("📦 Deployment Package Contents:")
    print(f"   Location: {deploy_dir}")
    print(f"   Executable: MediaVaultScanner.exe ({exe_size_mb:.2f} MB)")
    print(f"   Documentation: README.md, INSTALL.txt, LICENSE")
    print(f"   Scripts: download_model.ps1")
    print(f"   Models folder: Ready for GGUF model file")

    print(f"\n📦 Distribution Archive:")
    print(f"   File: {zip_path}")
    print(f"   Size: {zip_size_mb:.2f} MB")

    print("\n📋 Next Steps:")
    print("   1. Test the executable in the deployment folder")
    print("   2. Distribute the ZIP file to users")
    print("   3. Users follow INSTALL.txt instructions")

    print("\n🎉 MediaVault Scanner v2.0 is ready for distribution!")

def main():
    """Main deployment process"""
    print_header("MediaVault Scanner v2.0 - Deployment Package Creator")

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

    # Step 5: Create deployment package
    deploy_dir = create_deployment_package()

    # Step 6: Create ZIP archive
    zip_path = create_zip_archive(deploy_dir)

    # Print summary
    print_summary(deploy_dir, zip_path)

if __name__ == '__main__':
    main()


