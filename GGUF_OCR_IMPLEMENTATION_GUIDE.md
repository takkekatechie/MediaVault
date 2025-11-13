# MediaVault Scanner v2.0 - GGUF OCR Implementation Guide

## 🎯 Overview

MediaVault Scanner v2.0 now uses **GGUF-based OCR** via `llama-cpp-python` for high-performance text extraction with **cross-GPU support** (NVIDIA CUDA and AMD ROCm/HIP).

---

## 🚀 Key Features

### ✅ **Cross-GPU Acceleration**
- **NVIDIA CUDA**: Full GPU acceleration for NVIDIA GPUs
- **AMD ROCm/HIP**: Full GPU acceleration for AMD GPUs  
- **CPU Fallback**: Works without GPU (slower but functional)

### ✅ **Dual OCR Engine System**
1. **Primary**: Deepseek GGUF (high-performance, GPU-accelerated)
2. **Fallback**: Tesseract OCR (lightweight, CPU-only)

### ✅ **Intelligent Fallback**
- Automatically detects available OCR engines
- Falls back to Tesseract if GGUF model unavailable
- Graceful degradation with clear user feedback

---

## 📦 Installation

### **Step 1: Install llama-cpp-python**

#### **For NVIDIA CUDA (Recommended for NVIDIA GPUs)**

```powershell
# Windows PowerShell
$env:FORCE_CMAKE=1
$env:CMAKE_ARGS="-DLLAMA_CUBLAS=on"
pip install llama-cpp-python --no-cache-dir
```

#### **For AMD ROCm/HIP (For AMD GPUs)**

**Prerequisites**: AMD ROCm stack must be installed on your system.

```powershell
# Windows PowerShell
$env:FORCE_CMAKE=1
$env:CMAKE_ARGS="-DLLAMA_HIP=on"
pip install llama-cpp-python --no-cache-dir
```

#### **For CPU-Only (No GPU)**

```bash
pip install llama-cpp-python
```

---

### **Step 2: Obtain GGUF Model File**

1. Download a Deepseek OCR GGUF model file (e.g., `deepseek-ocr.gguf`)
2. Place it in the `models/` directory:
   ```
   MediaVault/
   ├── models/
   │   └── deepseek-ocr.gguf  ← Place model here
   ├── gguf_ocr.py
   ├── main.py
   └── ...
   ```

**Note**: The application will automatically create the `models/` directory if it doesn't exist.

---

### **Step 3: Install Tesseract (Fallback)**

1. Download Tesseract for Windows:  
   https://github.com/UB-Mannheim/tesseract/wiki

2. Run the installer (default path: `C:\Program Files\Tesseract-OCR`)

3. Add Tesseract to Windows PATH (recommended) or configure path in application

---

## 🔧 Configuration

### **Configuration File: `config.py`**

```python
# GGUF OCR Settings
DEEPSEEK_GGUF_PATH = "models/deepseek-ocr.gguf"  # Path to GGUF model file
MODEL_FOLDER = "models"  # Folder containing GGUF models

# GPU Acceleration Settings
USE_GPU = True  # Attempt to use GPU acceleration (CUDA or ROCm/HIP)
GPU_LAYERS = -1  # Number of layers to offload to GPU (-1 = all layers)
N_CTX = 2048  # Context window size
N_THREADS = 4  # Number of CPU threads (if GPU not available)

# OCR Engine Toggles
DEEPSEEK_ENABLED = True  # Enable/disable Deepseek GGUF OCR
TESSERACT_ENABLED = True  # Enable/disable Tesseract fallback
TESSERACT_PATH = None  # Path to Tesseract executable (auto-detected if None)
```

---

## 🧪 Testing

### **Run Test Script**

```bash
python test_gguf_ocr.py
```

**Expected Output**:
- Configuration summary
- Engine initialization status
- Model file detection
- GPU type detection (CUDA/ROCm/CPU)
- Installation instructions (if needed)

---

## 📊 Architecture

### **Module Structure**

```
MediaVault/
├── gguf_ocr.py              # GGUF OCR engine (NEW)
├── config.py                # Configuration management (UPDATED)
├── metadata_extractor.py    # Metadata extraction (UPDATED)
├── scanner.py               # Media scanner (UPDATED)
├── main.py                  # Main application (UPDATED)
├── model_setup_dialog.py    # Setup dialog (UPDATED)
└── test_gguf_ocr.py         # Test script (NEW)
```

### **Class: `GGUF_OCR`**

**File**: `gguf_ocr.py`

**Key Methods**:
- `__init__(config)` - Initialize OCR engine with config
- `extract_text(image, max_length)` - Extract text from image
- `get_engine_status()` - Get current engine status
- `_initialize_deepseek_gguf()` - Initialize GGUF model
- `_initialize_tesseract()` - Initialize Tesseract fallback
- `_detect_gpu_type()` - Detect GPU type (CUDA/ROCm/CPU)

---

## 🎮 Usage

### **Basic Usage**

```python
from gguf_ocr import GGUF_OCR
from config import Config

# Load configuration
config = Config.get_gguf_ocr_config()

# Initialize OCR engine
ocr = GGUF_OCR(config=config)

# Extract text from image
text_summary, keywords = ocr.extract_text("path/to/image.jpg", max_length=100)

print(f"Text: {text_summary}")
print(f"Keywords: {keywords}")
```

### **Check Engine Status**

```python
status = ocr.get_engine_status()

print(f"Current Engine: {status['current_engine']}")
print(f"Deepseek Available: {status['deepseek_available']}")
print(f"Tesseract Available: {status['tesseract_available']}")
print(f"GPU Type: {status['gpu_type']}")
```

---

## 🔍 Troubleshooting

### **Issue: "llama-cpp-python not installed"**

**Solution**: Install llama-cpp-python with GPU support (see Step 1 above)

### **Issue: "GGUF model file not found"**

**Solution**: Place the GGUF model file at `models/deepseek-ocr.gguf`

### **Issue: "Tesseract not available"**

**Solution**: Install Tesseract and add to PATH (see Step 3 above)

### **Issue: GPU not detected**

**Solution**:  
- **NVIDIA**: Ensure CUDA drivers are installed and `nvidia-smi` works
- **AMD**: Ensure ROCm stack is installed and `rocm-smi` works
- **Fallback**: Application will use CPU if GPU not detected

---

## 📝 Migration from PyTorch/Transformers

### **What Changed**

| Component | Old (v2.0 PyTorch) | New (v2.0 GGUF) |
|-----------|-------------------|-----------------|
| **Inference Engine** | PyTorch + transformers | llama-cpp-python |
| **Model Format** | HuggingFace (7GB+) | GGUF (2-7GB) |
| **GPU Support** | NVIDIA CUDA only | NVIDIA CUDA + AMD ROCm |
| **Module Name** | `vl_ocr.py` | `gguf_ocr.py` |
| **Class Name** | `VL_OCR` | `GGUF_OCR` |
| **Config Method** | `get_vl_ocr_config()` | `get_gguf_ocr_config()` |

### **Files Modified**

1. ✅ `config.py` - Updated for GGUF settings
2. ✅ `gguf_ocr.py` - New GGUF OCR module (replaces `vl_ocr.py`)
3. ✅ `metadata_extractor.py` - Updated to use `GGUF_OCR`
4. ✅ `scanner.py` - Updated parameter names
5. ✅ `main.py` - Updated to use `get_gguf_ocr_config()`
6. ✅ `model_setup_dialog.py` - Updated setup instructions

---

## 🎉 Summary

MediaVault Scanner v2.0 now supports:
- ✅ **Cross-GPU acceleration** (NVIDIA CUDA + AMD ROCm/HIP)
- ✅ **GGUF quantized models** (smaller, faster)
- ✅ **Intelligent fallback** to Tesseract
- ✅ **Easy configuration** via setup dialog
- ✅ **Comprehensive testing** with test script

**Ready for deployment!** 🚀

