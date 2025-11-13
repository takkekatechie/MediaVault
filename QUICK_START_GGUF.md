# MediaVault Scanner v2.0 - GGUF OCR Quick Start

## 🚀 Quick Installation (3 Steps)

### **Step 1: Install llama-cpp-python**

Choose ONE option based on your hardware:

#### **Option A: NVIDIA GPU (Recommended)**
```powershell
# Windows PowerShell
$env:FORCE_CMAKE=1
$env:CMAKE_ARGS="-DLLAMA_CUBLAS=on"
pip install llama-cpp-python --no-cache-dir
```

#### **Option B: AMD GPU**
**Prerequisites**: AMD ROCm stack must be installed.
```powershell
# Windows PowerShell
$env:FORCE_CMAKE=1
$env:CMAKE_ARGS="-DLLAMA_HIP=on"
pip install llama-cpp-python --no-cache-dir
```

#### **Option C: CPU Only (No GPU)**
```bash
pip install llama-cpp-python
```

---

### **Step 2: Place GGUF Model File**

1. Download Deepseek OCR GGUF model file (e.g., `deepseek-ocr.gguf`)
2. Create `models/` folder in MediaVault directory
3. Place model file at: `models/deepseek-ocr.gguf`

```
MediaVault/
├── models/
│   └── deepseek-ocr.gguf  ← Place model here
├── gguf_ocr.py
├── main.py
└── ...
```

---

### **Step 3: Install Tesseract (Fallback)**

1. Download: https://github.com/UB-Mannheim/tesseract/wiki
2. Install (default: `C:\Program Files\Tesseract-OCR`)
3. Add to Windows PATH (recommended)

---

## 🧪 Test Your Setup

```bash
python test_gguf_ocr.py
```

**Expected Output**:
- ✅ Configuration loaded
- ✅ Engine status (Deepseek/Tesseract/None)
- ✅ GPU type detected (CUDA/ROCm/CPU)
- ✅ Model file status
- ✅ Installation instructions (if needed)

---

## 🎮 Run the Application

```bash
python main.py
```

**On First Run**:
- Model Setup Dialog will appear
- Follow instructions for GGUF model placement
- Configure Tesseract path (if needed)
- Click "Continue to Application"

---

## 🔍 Troubleshooting

### **Issue: "llama-cpp-python not installed"**
**Solution**: Run Step 1 above

### **Issue: "GGUF model file not found"**
**Solution**: Place model file at `models/deepseek-ocr.gguf`

### **Issue: "Tesseract not available"**
**Solution**: Install Tesseract and add to PATH

### **Issue: GPU not detected**
**Solution**: 
- NVIDIA: Ensure CUDA drivers installed, run `nvidia-smi`
- AMD: Ensure ROCm stack installed, run `rocm-smi`
- Fallback: Application will use CPU

---

## 📊 Configuration

**File**: `config.py`

```python
# GGUF Model Settings
DEEPSEEK_GGUF_PATH = "models/deepseek-ocr.gguf"
MODEL_FOLDER = "models"

# GPU Settings
USE_GPU = True  # Enable GPU acceleration
GPU_LAYERS = -1  # -1 = all layers to GPU
N_CTX = 2048  # Context window size
N_THREADS = 4  # CPU threads

# OCR Engine Toggles
DEEPSEEK_ENABLED = True  # Enable Deepseek GGUF
TESSERACT_ENABLED = True  # Enable Tesseract fallback
TESSERACT_PATH = None  # Auto-detect or specify path
```

---

## 📝 Key Differences from v2.0 PyTorch

| Aspect | PyTorch Version | GGUF Version |
|--------|----------------|--------------|
| **Library** | PyTorch + transformers | llama-cpp-python |
| **Model** | HuggingFace (7GB+) | GGUF (2-7GB) |
| **GPU** | NVIDIA only | NVIDIA + AMD |
| **Setup** | Auto-download | Manual placement |
| **Size** | Large | Smaller |

---

## 🎯 What's New

### **Cross-GPU Support**
- ✅ NVIDIA CUDA acceleration
- ✅ AMD ROCm/HIP acceleration
- ✅ CPU fallback

### **GGUF Model Format**
- ✅ Quantized models (smaller size)
- ✅ Faster inference
- ✅ Better portability

### **Improved Setup Dialog**
- ✅ Clear GGUF model placement instructions
- ✅ GPU acceleration setup for both NVIDIA and AMD
- ✅ Tesseract fallback configuration

---

## 📚 Documentation

- **Implementation Guide**: `GGUF_OCR_IMPLEMENTATION_GUIDE.md`
- **Migration Summary**: `GGUF_MIGRATION_COMPLETE.md`
- **Test Script**: `test_gguf_ocr.py`

---

## 🎉 Summary

**MediaVault Scanner v2.0 with GGUF OCR is ready!**

1. ✅ Install llama-cpp-python (with GPU support)
2. ✅ Place GGUF model file
3. ✅ Install Tesseract (fallback)
4. ✅ Run test script
5. ✅ Launch application

**Enjoy high-performance OCR with cross-GPU support!** 🚀

