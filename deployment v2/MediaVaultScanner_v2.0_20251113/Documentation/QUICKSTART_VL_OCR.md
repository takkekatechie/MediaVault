# MediaVault Scanner v2.0 - Quick Start Guide

**Get started with Enhanced VL-OCR in 5 minutes!**

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Tesseract OCR (Required)

1. Download: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer: `tesseract-ocr-w64-setup-*.exe`
3. Add to Windows PATH (recommended)

**Verify Installation**:
```bash
tesseract --version
```

---

### Step 2: Optional - Install PyTorch for High-Performance OCR

**For GPU Acceleration** (Recommended):
```bash
# CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# Install transformers
pip install transformers accelerate sentencepiece protobuf
```

**For CPU-Only** (Slower):
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install transformers accelerate sentencepiece protobuf
```

**Skip This Step** if you want to use Tesseract-only mode (lightweight, no GPU needed).

---

### Step 3: Run MediaVault Scanner

**Option A: Executable**
```bash
MediaVaultScanner.exe
```

**Option B: Python**
```bash
python main.py
```

---

## 🎯 First Run: Model Setup Dialog

On first launch, you'll see a setup dialog with 3 sections:

### Section A: Deepseek-VL Setup (Optional)
- **If you installed PyTorch**: Configure model cache directory (optional)
- **If you skipped PyTorch**: This section will be informational only

### Section B: Tesseract Fallback
- Read about automatic fallback mechanism
- Verify Tesseract installation

### Section C: Tesseract Path
- Click **"Auto-Detect"** to find Tesseract automatically
- Or click **"Browse"** to select manually

### Choose Your Mode:

**High-Performance Mode** (Deepseek-VL):
- Click **"Continue to Application"**
- Model weights will download on first scan (~7GB, 10-30 min)
- Subsequent scans use cached model (instant)

**Lightweight Mode** (Tesseract-Only):
- Click **"Skip Setup (Use Tesseract Only)"**
- No model download needed
- Smaller memory footprint

---

## 📸 Scanning Your First Directory

1. **Browse**: Click "Browse" and select a folder with photos/videos
2. **Start Scan**: Click "Start Scan"
3. **Wait**: Watch progress bar (OCR engine shown in logs)
4. **Analyze**: View results in Analysis Dashboard

---

## 🔍 Understanding OCR Engines

### Deepseek-VL (Primary)
- **Accuracy**: ⭐⭐⭐⭐⭐ (Excellent)
- **Speed**: ⭐⭐⭐⭐ (Fast with GPU)
- **Requirements**: GPU with 6GB+ VRAM, 15GB disk space
- **Best For**: Complex text, handwriting, artistic fonts

### Tesseract (Fallback)
- **Accuracy**: ⭐⭐⭐ (Good)
- **Speed**: ⭐⭐⭐ (Moderate)
- **Requirements**: Minimal (works on any hardware)
- **Best For**: Clear printed text, simple layouts

### Automatic Fallback
The application automatically uses the best available engine:
```
Deepseek-VL available? → Use Deepseek
    ↓ No
Tesseract available? → Use Tesseract
    ↓ No
No OCR (other features still work)
```

---

## ⚙️ Configuration Tips

### Custom Model Cache Directory

If you have limited space on C: drive:

1. Launch application
2. In Model Setup Dialog, set "Model Cache Directory" to:
   ```
   D:\AI_Models\huggingface\
   ```
3. Click "Continue to Application"

### Tesseract Not Auto-Detected?

1. Find your Tesseract installation (usually `C:\Program Files\Tesseract-OCR`)
2. In Model Setup Dialog, click "Browse"
3. Navigate to Tesseract folder and select `tesseract.exe`
4. Click "Save Path & Continue"

### Disable Deepseek (Save Memory)

1. Launch application
2. In Model Setup Dialog, click "Skip Setup (Use Tesseract Only)"
3. Application will use Tesseract for all OCR

---

## 🎓 Usage Examples

### Example 1: Scan Family Photos (Deepseek-VL)

**Setup**:
- PyTorch installed with CUDA
- Deepseek-VL enabled
- 16GB RAM, NVIDIA GPU

**Workflow**:
1. Select folder: `C:\Users\John\Pictures\Family`
2. Start scan
3. First scan: Model downloads (~20 min)
4. Subsequent scans: Instant OCR processing
5. High-accuracy text extraction from photo captions

### Example 2: Quick Scan (Tesseract-Only)

**Setup**:
- Tesseract installed
- Deepseek disabled (lightweight mode)
- 4GB RAM, no GPU

**Workflow**:
1. Select folder: `C:\Users\Jane\Pictures\Vacation`
2. Start scan
3. Fast OCR processing with Tesseract
4. Good accuracy for clear text
5. Low memory usage

### Example 3: Large Archive (Mixed)

**Setup**:
- Both Deepseek and Tesseract installed
- Automatic fallback enabled

**Workflow**:
1. Select folder: `D:\PhotoArchive` (10,000+ files)
2. Start scan
3. Deepseek processes most files
4. Falls back to Tesseract if GPU memory full
5. Reliable processing of entire archive

---

## 🐛 Quick Troubleshooting

### "Tesseract not found"
- Install Tesseract from link above
- Add to Windows PATH
- Or specify path manually in setup dialog

### "Deepseek not working"
- Verify PyTorch installed: `python -c "import torch; print(torch.__version__)"`
- Check GPU: `python -c "import torch; print(torch.cuda.is_available())"`
- Ensure 15GB free disk space
- Check internet connection for model download

### "Model download stuck"
- Check internet connection
- Verify disk space
- Wait (large download, may take 30 min)
- Or use Tesseract-only mode

### "Out of memory"
- Close other applications
- Use Tesseract-only mode
- Or use CPU-only PyTorch (slower but works)

---

## 📚 Next Steps

- **Full Documentation**: See `README.md`
- **Deployment Guide**: See `VL_OCR_DEPLOYMENT_GUIDE.md`
- **Technical Details**: See `VL_OCR_IMPLEMENTATION_SUMMARY.md`
- **Testing**: Run `python test_vl_ocr.py`

---

## 🎉 You're Ready!

MediaVault Scanner v2.0 is now configured and ready to scan your media files with advanced VL-OCR capabilities!

**Happy Scanning! 📸🎥**

