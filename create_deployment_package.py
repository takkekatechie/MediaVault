"""
MediaVault Scanner v2.0 - Deployment Package Creator
Creates a complete deployment package with executable and documentation
"""

import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def create_deployment_package():
    """Create a complete deployment package"""
    print_header("MediaVault Scanner v2.0 - Deployment Package Creator")
    
    # Configuration
    package_name = f"MediaVaultScanner_v2.0_{datetime.now().strftime('%Y%m%d')}"
    package_dir = Path("deployment") / package_name
    
    # Files to include
    files_to_include = {
        'dist/MediaVaultScanner.exe': 'MediaVaultScanner.exe',
        'README.md': 'Documentation/README.md',
        'INSTALLATION_INSTRUCTIONS.md': 'INSTALLATION_INSTRUCTIONS.md',
        'QUICKSTART_VL_OCR.md': 'Documentation/QUICKSTART_VL_OCR.md',
        'VL_OCR_DEPLOYMENT_GUIDE.md': 'Documentation/VL_OCR_DEPLOYMENT_GUIDE.md',
        'FINAL_VL_OCR_SUMMARY.md': 'Documentation/FINAL_VL_OCR_SUMMARY.md',
    }
    
    print("Step 1: Creating package directory structure...")
    # Create package directory
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True, exist_ok=True)
    (package_dir / "Documentation").mkdir(exist_ok=True)
    
    print("✓ Directory structure created\n")
    
    print("Step 2: Copying files to package...")
    # Copy files
    missing_files = []
    for source, dest in files_to_include.items():
        source_path = Path(source)
        dest_path = package_dir / dest
        
        if source_path.exists():
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, dest_path)
            size_mb = source_path.stat().st_size / (1024 * 1024)
            print(f"  ✓ {source} → {dest} ({size_mb:.2f} MB)")
        else:
            missing_files.append(source)
            print(f"  ✗ {source} - NOT FOUND")
    
    if missing_files:
        print(f"\n⚠ Warning: {len(missing_files)} file(s) not found")
        print("Missing files:", ", ".join(missing_files))
    
    print("\n✓ Files copied\n")
    
    print("Step 3: Creating README for package...")
    # Create package README
    package_readme = package_dir / "README_FIRST.txt"
    with open(package_readme, 'w', encoding='utf-8') as f:
        f.write("""
================================================================================
  MediaVault Scanner v2.0 - Enhanced VL-OCR
================================================================================

Thank you for downloading MediaVault Scanner v2.0!

QUICK START:
-----------
1. Read INSTALLATION_INSTRUCTIONS.md for setup guide
2. Install Tesseract OCR (REQUIRED - see installation instructions)
3. Run MediaVaultScanner.exe
4. Complete the Model Setup Dialog on first run
5. Start scanning your photos and videos!

WHAT'S INCLUDED:
---------------
- MediaVaultScanner.exe (65 MB) - Main application
- INSTALLATION_INSTRUCTIONS.md - Step-by-step installation guide
- Documentation/ - Complete documentation and guides

SYSTEM REQUIREMENTS:
-------------------
Minimum (Tesseract-Only):
- Windows 10/11 (64-bit)
- 4GB RAM
- 500MB disk space
- Tesseract OCR

Recommended (With Deepseek-VL):
- Windows 10/11 (64-bit)
- 16GB RAM
- NVIDIA GPU with 6GB+ VRAM
- 15GB disk space
- CUDA 11.8 or 12.1
- Tesseract OCR + PyTorch

IMPORTANT:
---------
- Tesseract OCR must be installed separately (see INSTALLATION_INSTRUCTIONS.md)
- For high-performance OCR, install PyTorch (optional, see installation guide)
- On first run, complete the Model Setup Dialog
- Model weights (~7GB) download automatically if using Deepseek-VL

DOCUMENTATION:
-------------
- INSTALLATION_INSTRUCTIONS.md - Installation and setup
- Documentation/README.md - Complete feature documentation
- Documentation/QUICKSTART_VL_OCR.md - Quick start guide
- Documentation/VL_OCR_DEPLOYMENT_GUIDE.md - Advanced deployment

SUPPORT:
-------
For issues or questions, refer to the documentation files.

Version: 2.0.0 (Enhanced VL-OCR)
Build Date: """ + datetime.now().strftime('%Y-%m-%d') + """

Happy Scanning! 📸🎥
================================================================================
""")
    print("✓ Package README created\n")
    
    print("Step 4: Creating ZIP archive...")
    # Create ZIP file
    zip_path = Path("deployment") / f"{package_name}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arcname)
                print(f"  Adding: {arcname}")
    
    zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"\n✓ ZIP archive created: {zip_path} ({zip_size_mb:.2f} MB)\n")
    
    # Summary
    print_header("Deployment Package Complete!")
    print(f"📦 Package Directory: {package_dir}")
    print(f"📦 ZIP Archive: {zip_path} ({zip_size_mb:.2f} MB)")
    print(f"\n📋 Package Contents:")
    print(f"   - MediaVaultScanner.exe (65 MB)")
    print(f"   - INSTALLATION_INSTRUCTIONS.md")
    print(f"   - README_FIRST.txt")
    print(f"   - Documentation/ (5 files)")
    
    print(f"\n🚀 Ready for Distribution!")
    print(f"   1. Test the package on a clean Windows machine")
    print(f"   2. Distribute {zip_path.name}")
    print(f"   3. Users extract and follow INSTALLATION_INSTRUCTIONS.md")
    
    print(f"\n✅ Deployment package created successfully!")

if __name__ == '__main__':
    create_deployment_package()

