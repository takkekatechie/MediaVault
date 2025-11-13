# MediaVault Scanner - VL-OCR Deployment Guide

**Version**: 2.0.0 (Enhanced VL-OCR)  
**Date**: 2025-01-15  
**Status**: Production Ready with Advanced OCR

---

## 🎯 Overview

MediaVault Scanner v2.0 introduces **Vision-Language OCR (VL-OCR)** powered by Deepseek-VL, a state-of-the-art vision-language model that provides superior text extraction accuracy compared to traditional OCR methods.

### Key Features

- ✅ **Dual OCR Engine**: Deepseek-VL (primary) with Tesseract fallback
- ✅ **Automatic Fallback**: Seamlessly switches to Tesseract if Deepseek unavailable
- ✅ **GPU Acceleration**: Supports CUDA for high-performance processing
- ✅ **Flexible Deployment**: Multiple deployment strategies for different use cases

---

## 📦 Deployment Strategies

### Strategy A: Full Bundle (Recommended for Power Users)

**Pros:**
- Everything included in one executable
- Best OCR performance out-of-the-box
- No additional setup required (except Tesseract)

**Cons:**
- Very large executable size (~3-4GB)
- Long build time
- Requires significant disk space

**Build Command:**
```bash
pyinstaller mediavault.spec
```

**Executable Size:** ~3-4GB  
**First Run:** Downloads Deepseek model weights (~7GB) to user cache

---

### Strategy B: Lightweight Bundle (Recommended for Distribution)

**Pros:**
- Smaller executable size (~100-200MB)
- Faster build time
- Easier to distribute

**Cons:**
- Users must install PyTorch/transformers separately
- Requires additional setup steps

**Build Command:**
1. Edit `mediavault.spec` and uncomment these lines in the `excludes` section:
   ```python
   'torch',
   'torchvision',
   'transformers',
   ```

2. Build:
   ```bash
   pyinstaller mediavault.spec
   ```

**User Installation:**
Users must run:
```bash
# For CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# For CPU-only
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install transformers
pip install transformers accelerate sentencepiece protobuf
```

---

### Strategy C: Python Environment (Recommended for Developers)

**Pros:**
- No executable build needed
- Easy to update and maintain
- Full control over dependencies

**Cons:**
- Requires Python installation
- Users must manage dependencies

**Setup:**
```bash
# Clone or download the repository
cd MediaVault

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

---

## 🔧 System Requirements

### Minimum Requirements (Tesseract Only)
- **OS**: Windows 10/11 (64-bit)
- **RAM**: 4GB
- **Disk Space**: 500MB
- **GPU**: Not required

### Recommended Requirements (Deepseek-VL)
- **OS**: Windows 10/11 (64-bit)
- **RAM**: 16GB
- **Disk Space**: 15GB (10GB for model weights + 5GB for application)
- **GPU**: NVIDIA GPU with 6GB+ VRAM
- **CUDA**: 11.8 or 12.1

---

## 📥 Model Weights Management

### Automatic Download (Default)

On first run with Deepseek-VL enabled, the application will automatically download model weights:

**Download Location:**
```
Windows: C:\Users\<Username>\.cache\huggingface\hub\
```

**Download Size:** ~7GB  
**Download Time:** 10-30 minutes (depending on internet speed)

### Custom Cache Directory

Users can specify a custom cache directory in the Model Setup Dialog:

1. Launch application
2. In Model Setup Dialog, set "Model Cache Directory"
3. Click "Continue to Application"

**Example Custom Path:**
```
D:\AI_Models\huggingface\
```

### Pre-downloading Models (Optional)

For offline deployment or faster first run:

```bash
# Pre-download Deepseek-VL model
python -c "from transformers import AutoModelForVision2Seq, AutoProcessor; \
AutoProcessor.from_pretrained('deepseek-ai/deepseek-vl-7b-chat', trust_remote_code=True); \
AutoModelForVision2Seq.from_pretrained('deepseek-ai/deepseek-vl-7b-chat', trust_remote_code=True)"
```

---

## 🔄 Fallback Mechanism

The application implements intelligent fallback:

```
1. Try Deepseek-VL
   ├─ Success → Use Deepseek for OCR
   └─ Failure (missing deps, no GPU, etc.)
      └─ 2. Try Tesseract
         ├─ Success → Use Tesseract for OCR
         └─ Failure → No OCR available (warning shown)
```

### Fallback Triggers

Deepseek-VL will fall back to Tesseract if:
- PyTorch not installed
- Transformers not installed
- Insufficient GPU memory
- Model download failed
- User disabled Deepseek in settings

---

## 🛠️ Building the Executable

### Prerequisites

```bash
# Install all dependencies
pip install -r requirements.txt

# Verify PyInstaller
pyinstaller --version
```

### Build Process

**Step 1: Choose Deployment Strategy**
- Edit `mediavault.spec` if using Strategy B (lightweight)

**Step 2: Run PyInstaller**
```bash
pyinstaller mediavault.spec
```

**Step 3: Verify Build**
```bash
# Check executable
dir dist\MediaVaultScanner.exe

# Test run
dist\MediaVaultScanner.exe
```

### Build Time Estimates

| Strategy | Build Time | Executable Size |
|----------|------------|-----------------|
| Full Bundle (A) | 15-30 min | 3-4GB |
| Lightweight (B) | 5-10 min | 100-200MB |
| Python Env (C) | N/A | N/A |

---

## 📋 User Installation Instructions

### For End Users (Strategy A - Full Bundle)

**Step 1: Install Tesseract OCR**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer: `tesseract-ocr-w64-setup-*.exe`
3. Add to Windows PATH (recommended)

**Step 2: Run MediaVault Scanner**
1. Double-click `MediaVaultScanner.exe`
2. Complete Model Setup Dialog
3. Start scanning!

**First Run Notes:**
- Deepseek model will download automatically (~7GB, 10-30 min)
- Application will show download progress
- Subsequent runs will be instant

---

### For End Users (Strategy B - Lightweight)

**Step 1: Install Python Dependencies**
```bash
# Install PyTorch (choose one)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118  # CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121  # CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu    # CPU-only

# Install transformers
pip install transformers accelerate sentencepiece protobuf
```

**Step 2: Install Tesseract OCR**
(Same as Strategy A)

**Step 3: Run MediaVault Scanner**
(Same as Strategy A)

---

## 🧪 Testing the Build

### Test Checklist

- [ ] Application launches without errors
- [ ] Model Setup Dialog appears on first run
- [ ] Tesseract auto-detection works
- [ ] Can browse and select directories
- [ ] Scan completes successfully
- [ ] Deepseek-VL OCR works (if available)
- [ ] Tesseract fallback works
- [ ] Analysis dashboard displays correctly
- [ ] CSV export works
- [ ] Thumbnails display correctly
- [ ] Click-to-open files works

### Test Commands

```bash
# Test Deepseek availability
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}')"

# Test transformers
python -c "from transformers import AutoProcessor; print('Transformers OK')"

# Test Tesseract
python -c "import pytesseract; print(pytesseract.get_tesseract_version())"
```

---

## ⚠️ Known Issues & Limitations

### Deepseek-VL Limitations

1. **Large Model Size**: 7GB download required
2. **GPU Memory**: Requires 6GB+ VRAM for optimal performance
3. **First Run Delay**: Model download takes 10-30 minutes
4. **CPU Performance**: Very slow on CPU-only systems (use Tesseract instead)

### PyInstaller Limitations

1. **Executable Size**: Full bundle is 3-4GB
2. **Build Time**: Can take 15-30 minutes
3. **Antivirus False Positives**: Some antivirus may flag the executable

### Workarounds

**Issue**: Executable too large  
**Solution**: Use Strategy B (lightweight bundle)

**Issue**: Deepseek too slow on CPU  
**Solution**: Disable Deepseek in Model Setup Dialog, use Tesseract only

**Issue**: Model download fails  
**Solution**: Check internet connection, try manual download, or use Tesseract fallback

---

## 📞 Support & Troubleshooting

### Common Issues

**Q: Application won't start**  
A: Check Windows Event Viewer for errors, ensure all dependencies installed

**Q: Deepseek not working**  
A: Verify PyTorch/CUDA installation, check GPU memory, try CPU-only mode

**Q: Tesseract not found**  
A: Install Tesseract, add to PATH, or specify path in Model Setup Dialog

**Q: Model download stuck**  
A: Check internet connection, verify disk space, try manual download

---

## 🎉 Deployment Checklist

- [ ] Choose deployment strategy (A, B, or C)
- [ ] Update `mediavault.spec` if needed
- [ ] Build executable with PyInstaller
- [ ] Test executable on clean Windows system
- [ ] Prepare user documentation
- [ ] Include Tesseract installation instructions
- [ ] Include PyTorch installation instructions (if Strategy B)
- [ ] Test Deepseek-VL functionality
- [ ] Test Tesseract fallback
- [ ] Package and distribute

---

**MediaVault Scanner v2.0 with VL-OCR is ready for deployment! 🚀**

