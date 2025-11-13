# MediaVault Scanner v2.0 - Installation Instructions

**Welcome to MediaVault Scanner v2.0 with Enhanced VL-OCR!**

This guide will help you install and run MediaVault Scanner on your Windows computer.

---

## 📋 System Requirements

### Minimum (Tesseract-Only Mode)
- Windows 10 or Windows 11 (64-bit)
- 4GB RAM
- 500MB free disk space
- Tesseract OCR (installation instructions below)

### Recommended (With Deepseek-VL)
- Windows 10 or Windows 11 (64-bit)
- 16GB RAM
- NVIDIA GPU with 6GB+ VRAM
- 15GB free disk space (10GB for model weights)
- CUDA 11.8 or 12.1
- Tesseract OCR + PyTorch (installation instructions below)

---

## 🚀 Quick Installation (3 Steps)

### Step 1: Install Tesseract OCR (REQUIRED)

Tesseract is required for text extraction from images and videos.

1. **Download Tesseract**:
   - Visit: https://github.com/UB-Mannheim/tesseract/wiki
   - Download: `tesseract-ocr-w64-setup-5.3.3.20231005.exe` (or latest version)

2. **Run the installer**:
   - Double-click the downloaded file
   - Follow the installation wizard
   - **Note the installation path** (default: `C:\Program Files\Tesseract-OCR`)

3. **Add to Windows PATH** (Recommended):
   - Open Windows Settings → System → About
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", find and select "Path"
   - Click "Edit" → "New"
   - Add: `C:\Program Files\Tesseract-OCR`
   - Click OK on all dialogs
   - **Restart your computer** for changes to take effect

4. **Verify installation**:
   - Open Command Prompt
   - Type: `tesseract --version`
   - You should see version information

---

### Step 2: Run MediaVault Scanner

1. **Extract the ZIP file** (if downloaded as ZIP)
2. **Navigate to the folder** containing `MediaVaultScanner.exe`
3. **Double-click** `MediaVaultScanner.exe`

**On first run**, you'll see a Model Setup Dialog:
- Section A: Deepseek-VL setup (optional, see Step 3)
- Section B: Tesseract fallback information
- Section C: Tesseract path configuration

**For Tesseract-only mode**:
- Click "Auto-Detect" to find Tesseract automatically
- Or click "Browse" to select Tesseract manually
- Click "Skip Setup (Use Tesseract Only)"

The application will now launch and you can start scanning!

---

### Step 3: Optional - Install PyTorch for High-Performance OCR

If you want to use **Deepseek-VL** for superior text extraction accuracy, follow these steps:

**Prerequisites**:
- NVIDIA GPU with 6GB+ VRAM
- CUDA 11.8 or 12.1 installed
- 15GB free disk space

**Installation**:

1. **Install Python 3.10 or higher** (if not already installed):
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Open Command Prompt** and install PyTorch:

   **For CUDA 11.8**:
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

   **For CUDA 12.1**:
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
   ```

   **For CPU-only** (slower, not recommended):
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
   ```

3. **Install transformers and dependencies**:
   ```bash
   pip install transformers accelerate sentencepiece protobuf
   ```

4. **Restart MediaVault Scanner**:
   - Close the application if running
   - Launch `MediaVaultScanner.exe` again
   - In the Model Setup Dialog, configure Deepseek-VL settings
   - Click "Continue to Application"

5. **First scan with Deepseek-VL**:
   - Model weights will download automatically (~7GB, 10-30 minutes)
   - Subsequent scans will be instant (model cached)

---

## 📸 Using MediaVault Scanner

### Scanning Your First Directory

1. **Launch the application**: Double-click `MediaVaultScanner.exe`
2. **Browse**: Click "Browse" and select a folder with photos/videos
3. **Start Scan**: Click "Start Scan"
4. **Wait**: Watch the progress bar
5. **Analyze**: View results in the Analysis Dashboard

### Features

- **Metadata Extraction**: EXIF data, GPS coordinates, timestamps
- **Face Detection**: Automatic person counting
- **OCR Text Extraction**: Extract text from images and videos
- **Object Detection**: Identify scenes (sky, grass, water, etc.)
- **Emotion Analysis**: Sentiment heuristics
- **Interactive Thumbnails**: Click to open files
- **Data Filtering**: Filter by emotion, person count, keywords
- **CSV Export**: Export results to spreadsheet

---

## 🔍 OCR Modes

MediaVault Scanner supports two OCR modes:

### Mode 1: Tesseract-Only (Lightweight)
- **Accuracy**: Good for clear printed text
- **Speed**: Moderate
- **Requirements**: Just Tesseract OCR
- **Memory**: Low (works on any hardware)

### Mode 2: Deepseek-VL + Tesseract (High-Performance)
- **Accuracy**: Excellent for all text types
- **Speed**: Fast with GPU
- **Requirements**: PyTorch + CUDA + Tesseract
- **Memory**: High (needs GPU with 6GB+ VRAM)

The application automatically uses the best available mode.

---

## 🐛 Troubleshooting

### "Tesseract not found" error
- Verify Tesseract is installed at `C:\Program Files\Tesseract-OCR`
- Check Windows PATH includes Tesseract directory
- Try manual path specification in Model Setup Dialog
- Restart computer after PATH changes

### Application won't start
- Right-click `MediaVaultScanner.exe` → Properties
- Check "Unblock" if present → Apply
- Run as Administrator (right-click → Run as administrator)

### Deepseek-VL not working
- Verify PyTorch installed: `python -c "import torch; print(torch.__version__)"`
- Check GPU available: `python -c "import torch; print(torch.cuda.is_available())"`
- Ensure 15GB free disk space
- Check internet connection for model download

### Model download stuck
- Check internet connection
- Verify disk space (need 10GB free)
- Wait patiently (large download, may take 30 minutes)
- Or use Tesseract-only mode

---

## 📚 Additional Resources

- **README.md** - Complete documentation
- **QUICKSTART_VL_OCR.md** - Quick start guide
- **VL_OCR_DEPLOYMENT_GUIDE.md** - Advanced deployment options

---

## 🎉 You're Ready!

MediaVault Scanner v2.0 is now installed and ready to scan your media files!

**Happy Scanning! 📸🎥**

---

## 📞 Support

For issues or questions:
- Check the troubleshooting section above
- Review the documentation files
- Check the GitHub repository for updates

**Version**: 2.0.0 (Enhanced VL-OCR)  
**Build Date**: 2025-01-15

