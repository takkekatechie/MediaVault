# MediaVault Scanner v2.0

**An Enthusiast project - Local Photo/Video Metadata Repository with Enhanced GGUF OCR**

MediaVault Scanner is a complete, self-contained Python desktop application designed to recursively scan local directories for image and video files, extract comprehensive metadata (including EXIF data, GPS coordinates, face detection, **advanced GGUF OCR text extraction**, and emotion heuristics), and persist this information into a structured SQLite database.

**🆕 NEW in v2.0**: **GGUF OCR** powered by Deepseek GGUF model via llama-cpp-python for high-performance text extraction with cross-GPU support (NVIDIA CUDA & AMD ROCm/HIP) and intelligent Tesseract fallback!

---

## 🎯 Features

### 🆕 Enhanced GGUF OCR (v2.0)
- **Dual OCR Engine System**:
  - **Primary**: Deepseek GGUF (quantized) model via llama-cpp-python for superior text extraction accuracy
  - **Fallback**: Tesseract OCR for lightweight, reliable text extraction
  - **Intelligent Fallback**: Automatically switches to Tesseract if Deepseek GGUF is not available
- **Cross-GPU Acceleration**: Supports both NVIDIA CUDA and AMD ROCm/HIP for high-performance OCR processing
- **On-Screen Setup Guide**: Comprehensive model setup dialog with step-by-step instructions
- **Flexible Configuration**: Custom GGUF model paths and Tesseract paths
- **Efficient Model Format**: GGUF quantized models (~2-7GB depending on quantization level)

### Scanning & Metadata Extraction
- **Recursive Directory Scanning**: Automatically finds all supported media files in a directory tree
- **Deep Metadata Extraction**:
  - EXIF data (timestamps, camera settings)
  - GPS coordinates (latitude/longitude in decimal format)
  - Face detection (person count using OpenCV)
  - **Advanced OCR text extraction** (using Deepseek GGUF via llama-cpp-python or Tesseract)
  - **Object/scene detection**: Local heuristic identification of natural scenes (sky, grass, water, sunset, foliage), structured objects (buildings), and circular objects, combined with OCR keywords
  - Emotion/sentiment heuristics (based on filename, location, and time-of-day)
- **SQLite Database**: Persistent, file-based storage with efficient indexing
- **Modern GUI**: Built with CustomTkinter for a sleek, dark-mode interface
- **Real-time Progress Tracking**: Visual feedback during scanning operations
- **Idempotent Operations**: Skip or update existing records
- **Windows Native**: Optimized for Windows 10/11

### Analysis & Export Dashboard (NEW!)
- **Interactive Analytics Dashboard**: Automatically displayed after scan completion
- **Key Insights Panel**:
  - Total files scanned (images/videos breakdown)
  - Geographic distribution summary (unique GPS locations)
  - Average people per photo (from face detection)
  - Dominant emotion/sentiment classification with percentages
  - Top 3 most frequent OCR keywords
- **Interactive Data Table with Thumbnails** (NEW!):
  - 64x64 pixel thumbnail previews for all media files
  - Video thumbnails captured at 5-second mark
  - Click any thumbnail or row to open file in default viewer
  - Visual preview before opening files
- **Smart Data Filtering**:
  - Filter by emotion/sentiment (Positive, Neutral, Negative)
  - Filter by person count range (min/max)
  - Search by keywords in OCR text
  - Real-time table updates based on filters
- **CSV Export Functionality**:
  - Export all records or only filtered subset
  - User-selectable save location
  - Includes all 12 metadata fields (including thumbnail path)

---

## 📋 Supported File Formats

- **Images**: `.jpg`, `.jpeg`, `.png`, `.heic`
- **Videos**: `.mp4`, `.mov`, `.avi`

---

## 🔧 System Requirements

### Minimum Requirements (Tesseract Only)
- **Operating System**: Windows 10 or Windows 11 (64-bit)
- **RAM**: 4GB
- **Disk Space**: 500MB
- **Python**: 3.10 or higher (for development)
- **Tesseract OCR**: Required for text extraction fallback

### Recommended Requirements (Deepseek GGUF)
- **Operating System**: Windows 10 or Windows 11 (64-bit)
- **RAM**: 8GB (16GB recommended)
- **Disk Space**: 10GB (2-7GB for GGUF model + 3GB for application)
- **GPU**: NVIDIA GPU with 4GB+ VRAM OR AMD GPU with ROCm support
- **CUDA/ROCm**: CUDA 11.8+ or ROCm 5.0+ (for GPU acceleration)
- **Python**: 3.10 or higher (for development)

---

## 📦 Installation

### Option 1: Using the Pre-built Executable (Recommended for End Users)

1. **Download the executable**:
   - Download the latest `MediaVaultScanner.exe` from the releases page

2. **Install Tesseract OCR** (Required):
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Run installer: `tesseract-ocr-w64-setup-*.exe`
   - Add to Windows PATH (recommended)

3. **Optional: Install llama-cpp-python with GPU support** (For high-performance OCR):

   **For NVIDIA CUDA (Windows PowerShell):**
   ```powershell
   $env:FORCE_CMAKE=1
   $env:CMAKE_ARGS="-DLLAMA_CUBLAS=on"
   pip install llama-cpp-python --no-cache-dir
   ```

   **For AMD ROCm/HIP (Windows PowerShell - requires ROCm stack installed):**
   ```powershell
   $env:FORCE_CMAKE=1
   $env:CMAKE_ARGS="-DLLAMA_HIP=on"
   pip install llama-cpp-python --no-cache-dir
   ```

   **For CPU-only (slower):**
   ```bash
   pip install llama-cpp-python
   ```

4. **Download the GGUF model**:
   - Place the Deepseek GGUF model file at `models/deepseek-ocr.gguf`
   - See the "Model Weights & Large Files" section below for download instructions

5. **Run the application**:
   - Double-click `MediaVaultScanner.exe`
   - Complete the Model Setup Dialog on first run
   - Start scanning!

**Note**: The GGUF model file must be downloaded separately and placed in the `models/` folder. See the download script in `scripts/download_model.ps1`.

### Option 2: Running from Source (For Developers)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/MediaVault.git
   cd MediaVault
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   **Note**: This will install all dependencies, including PyTorch and transformers. For CUDA support, see the PyTorch installation section below.

4. **Install Tesseract OCR** (see detailed instructions below)

5. **Run the application**:
   ```bash
   python main.py
   ```

---

## 🔍 OCR Engine Installation

MediaVault Scanner v2.0 supports two OCR engines with automatic fallback:

### Primary: Deepseek GGUF (High-Performance, Optional)

**Deepseek GGUF** is a quantized vision-language model that provides superior text extraction accuracy with efficient memory usage and cross-GPU support.

**Installation**:

1. **Install llama-cpp-python with GPU support**:

   **For NVIDIA CUDA (Windows PowerShell):**
   ```powershell
   $env:FORCE_CMAKE=1
   $env:CMAKE_ARGS="-DLLAMA_CUBLAS=on"
   pip install llama-cpp-python --no-cache-dir
   ```

   **For AMD ROCm/HIP (Windows PowerShell - requires ROCm stack installed):**
   ```powershell
   $env:FORCE_CMAKE=1
   $env:CMAKE_ARGS="-DLLAMA_HIP=on"
   pip install llama-cpp-python --no-cache-dir
   ```

   **Note for AMD users**: You must install the AMD ROCm software stack first: https://rocm.docs.amd.com/

   **For CPU-only (slower, not recommended):**
   ```bash
   pip install llama-cpp-python
   ```

2. **Download the GGUF model file**:
   - Download the Deepseek GGUF model (~2-7GB depending on quantization)
   - Place it at `models/deepseek-ocr.gguf`
   - Use the provided download script: `.\scripts\download_model.ps1 -Url "<MODEL_URL>" -OutPath "models\deepseek-ocr.gguf"`

**Requirements**:
- NVIDIA GPU with 4GB+ VRAM OR AMD GPU with ROCm support (recommended)
- 8GB RAM (16GB recommended)
- 10GB disk space (2-7GB for GGUF model)
- CUDA 11.8+ or ROCm 5.0+ (for GPU acceleration)

**Note**: If Deepseek GGUF is not available, the application will automatically fall back to Tesseract.

### Fallback: Tesseract OCR (Lightweight, Required)

**Tesseract** is a reliable, lightweight OCR engine that works on any hardware. It serves as the fallback when Deepseek GGUF is unavailable.

**Installation**:

### Step 1: Download and Install Tesseract

1. Visit the official Tesseract Windows installer page:
   - **URL**: https://github.com/UB-Mannheim/tesseract/wiki

2. Download the latest Windows installer:
   - Look for `tesseract-ocr-w64-setup-*.exe` (64-bit version)

3. Run the installer:
   - Follow the installation wizard
   - **Note the installation path** (default: `C:\Program Files\Tesseract-OCR`)
   - Complete the installation

### Step 2: Add Tesseract to Windows System PATH (RECOMMENDED)

This is the **preferred method** as it allows MediaVault to automatically detect Tesseract:

1. Open **Windows Settings** → **System** → **About**
2. Click **"Advanced system settings"**
3. Click **"Environment Variables"**
4. Under **"System variables"**, find and select **"Path"**
5. Click **"Edit"**
6. Click **"New"**
7. Add the Tesseract installation path:
   ```
   C:\Program Files\Tesseract-OCR
   ```
8. Click **"OK"** on all dialogs
9. **RESTART** MediaVault Scanner for changes to take effect

### Step 3: Alternative - Manual Path Configuration

If you prefer not to modify the system PATH:

1. Launch MediaVault Scanner
2. When prompted, click **"Browse"** in the Tesseract setup dialog
3. Navigate to your Tesseract installation and select `tesseract.exe`
4. Click **"Save Path & Continue"**

### Verification

- After installation, MediaVault will automatically detect Tesseract if it's in the PATH
- If not detected, you'll see a setup dialog on first launch
- OCR features will be enabled once Tesseract is properly configured

---

## 🚀 Usage

### First Run: Model Setup

On first launch, you'll see the **Model Setup Dialog** with three sections:

**Section A: Deepseek GGUF Setup (Optional)**
- Information about high-performance OCR with Deepseek GGUF
- llama-cpp-python installation instructions for NVIDIA CUDA and AMD ROCm/HIP
- GGUF model file path configuration

**Section B: Tesseract Fallback**
- Explanation of automatic fallback mechanism
- Tesseract installation instructions

**Section C: Tesseract Path Configuration**
- Auto-detect Tesseract installation
- Manual path specification if needed

**Options**:
- **Continue to Application**: Save settings and proceed
- **Skip Setup (Use Tesseract Only)**: Disable Deepseek GGUF, use lightweight Tesseract only

### Scanning Media Files

1. **Launch the application**:
   - Run `MediaVaultScanner.exe` (executable) or `python main.py` (source)
   - Complete Model Setup Dialog (first run only)

2. **Select a target directory**:
   - Click the **"Browse"** button
   - Choose the folder containing your photos and videos

3. **Configure scan options**:
   - **"Update existing records"** is checked by default (recommended for idempotency)
   - Uncheck to skip previously scanned files

4. **Start scanning**:
   - Click **"Start Scan"**
   - Monitor progress in real-time
   - OCR engine status shown in logs (Deepseek GGUF or Tesseract)
   - View results in the data table

5. **Stop scanning** (optional):
   - Click **"Stop Scan"** to halt the process
   - Automatically transitions to Analysis Dashboard

**Note**: The GGUF model file must be downloaded and placed in the `models/` folder before first use. See the download script in `scripts/download_model.ps1`.

### Using the Analysis Dashboard

After completing or stopping a scan, you'll automatically be taken to the **Analysis & Export Dashboard**:

1. **View Key Insights**:
   - Review the summary cards on the left panel
   - See total files, geographic distribution, average people per photo
   - Check dominant emotion/sentiment and top keywords

2. **Filter Your Data**:
   - **Emotion Filter**: Select Positive, Neutral, Negative, or All
   - **Person Count**: Enter min/max values to filter by number of people
   - **Keyword Search**: Type keywords to search in OCR text
   - Click **"Apply Filters"** to update the table

3. **Export Data**:
   - Click **"📊 Export Data"** button
   - Choose to export **All Records** or **Filtered Records Only**
   - Select save location and filename
   - Data exported as CSV with all 11 metadata fields

4. **Return to Scanning**:
   - Click **"← Back to Scan"** to return to the scan screen
   - Select a new directory or re-scan existing data

---

## 🗄️ Database Schema

The application creates a SQLite database (`metadata.db`) with the following structure:

```sql
CREATE TABLE media_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filepath TEXT UNIQUE NOT NULL,
    filename TEXT,
    file_type TEXT,
    date_time_original TEXT,
    gps_latitude REAL,
    gps_longitude REAL,
    person_count INTEGER,
    ocr_text_summary TEXT,
    object_keywords TEXT,
    emotion_sentiment TEXT,
    thumbnail_path TEXT
);
```

**Field Descriptions:**
- `id`: Auto-incrementing primary key
- `filepath`: Full path to the media file (unique)
- `filename`: File name only
- `file_type`: Type of file (Image/Video)
- `date_time_original`: Original date/time from EXIF
- `gps_latitude`: GPS latitude in decimal format
- `gps_longitude`: GPS longitude in decimal format
- `person_count`: Number of detected faces
- `ocr_text_summary`: Extracted OCR text (first 100 characters)
- `object_keywords`: **Combined list** of detected objects/scenes AND OCR keywords (NEW!)
- `emotion_sentiment`: Emotion/sentiment classification
- `thumbnail_path`: Path to 64x64 thumbnail image

---

## 🎨 Object/Scene Detection (Local Heuristic)

MediaVault Scanner includes a **simplified local heuristic** for object and scene detection. This is **NOT** a cloud-based ML service, but a pattern-recognition system using OpenCV.

### Detection Methods

**1. Color-Based Scene Detection**
- Analyzes dominant colors in HSV color space
- Detects natural scenes:
  - **Sky**: Blue hues (>15% of image)
  - **Grass/Foliage**: Green hues (>15% of image)
  - **Water**: Cyan/blue hues (>15% of image)
  - **Sunset**: Orange/red hues (>15% of image)

**2. Edge-Based Object Detection**
- Uses Canny edge detection
- Identifies structured objects:
  - **Buildings/Structures**: High edge density (>10%)

**3. Shape Detection**
- Hough Circle Transform
- Detects circular objects (faces, balls, wheels, etc.)

**4. OCR Keyword Integration**
- Combines detected objects with OCR-extracted keywords
- Stored together in `object_keywords` field
- Example: `"sky, grass, building/structure, vacation, beach, summer"`

### Important Notes
- This is a **basic pattern recognition system**, not ML-based detection
- Best suited for identifying common scenes and environments
- Results are combined with OCR keywords for comprehensive tagging
- For videos, detection runs on the 5-second frame sample

---

## 📦 Building the Executable (For Developers)

To create a standalone Windows executable using PyInstaller:

### Method 1: Using the Provided Spec File

```bash
pyinstaller mediavault.spec
```

### Method 2: Manual Build Command

```bash
pyinstaller --name=MediaVaultScanner ^
            --onefile ^
            --windowed ^
            --icon=icon.ico ^
            --add-data="haarcascade_frontalface_default.xml;." ^
            main.py
```

The executable will be created in the `dist` folder.

### Important Notes for Deployment:

1. **PyTorch/Transformers**: Large dependencies (~2-4GB) - consider lightweight build strategy
2. **Model Weights**: NOT bundled - downloaded on first run (~7GB)
3. **Tesseract**: NOT bundled - users must install separately
4. **Test the executable**: Always test on a clean Windows machine
5. **Deployment Strategies**: See `VL_OCR_DEPLOYMENT_GUIDE.md` for detailed options

**For detailed deployment instructions, see**: [`VL_OCR_DEPLOYMENT_GUIDE.md`](VL_OCR_DEPLOYMENT_GUIDE.md)

---

## 🛠️ Technology Stack

### Core Technologies
- **Language**: Python 3.10+
- **GUI Framework**: CustomTkinter (modern, dark-mode UI)
- **Database**: SQLite3 (built-in)
- **Packaging**: PyInstaller

### GGUF OCR (v2.0)
- **Primary OCR**: Deepseek GGUF (quantized vision-language model)
- **Inference Engine**: llama-cpp-python (cross-GPU support: NVIDIA CUDA & AMD ROCm/HIP)
- **Model Format**: GGUF (efficient quantized format)
- **Fallback OCR**: pytesseract (Tesseract wrapper)

### Media Processing
- **Image Processing**: Pillow (PIL), exifread
- **Computer Vision**: opencv-python (face detection, object detection)
- **Video Processing**: opencv-python (frame extraction)

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## ⚠️ Troubleshooting

### Deepseek GGUF Not Working

**Problem**: Application falls back to Tesseract instead of using Deepseek GGUF

**Solution**:
- Verify llama-cpp-python is installed: `python -c "import llama_cpp; print(llama_cpp.__version__)"`
- Check if GGUF model file exists at `models/deepseek-ocr.gguf`
- Verify GPU availability (NVIDIA): `nvidia-smi` or (AMD): `rocm-smi`
- Ensure sufficient disk space for GGUF model (~2-7GB)
- Check that llama-cpp-python was compiled with GPU support
- Review logs for specific error messages

### GGUF Model File Missing

**Problem**: Application cannot find the GGUF model file

**Solution**:
- Download the Deepseek GGUF model file
- Place it at `models/deepseek-ocr.gguf`
- Use the download script: `.\scripts\download_model.ps1 -Url "<MODEL_URL>" -OutPath "models\deepseek-ocr.gguf"`
- Verify the file exists and is not corrupted
- Check file permissions

### Tesseract Not Found Error

**Problem**: Application shows "Tesseract not found" warning

**Solution**:
- Verify Tesseract is installed at `C:\Program Files\Tesseract-OCR`
- Check that Tesseract is in your system PATH
- Try manually specifying the path in the Model Setup Dialog
- Restart the application after making changes

### GPU Out of Memory

**Problem**: GPU runs out of memory when using Deepseek GGUF

**Solution**:
- Close other GPU-intensive applications
- Use CPU-only mode (slower but works): Set `use_gpu = False` in config
- Try a more quantized GGUF model (smaller file size = less VRAM)
- Reduce `gpu_layers` in config to offload fewer layers to GPU
- Use Tesseract-only mode for lower memory usage

### No Faces Detected

**Problem**: Person count is always 0

**Solution**:
- Face detection works best on clear, front-facing photos
- Ensure images have sufficient resolution
- Video face detection samples only one frame (at 5 seconds)

### OCR Returns Empty Results

**Problem**: No text is extracted from images

**Solution**:
- Ensure images contain clear, readable text
- Check that Tesseract is properly configured
- Try images with larger, higher-contrast text

### Database Locked Error

**Problem**: "Database is locked" error during scan

**Solution**:
- Close any other applications accessing `metadata.db`
- Ensure you're not running multiple instances of MediaVault
- Restart the application

---

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**MediaVault Scanner** - Your local media metadata repository solution.
##  Model Weights & Large Files

- **Note:** Large model weights and generated deployment artifacts are intentionally not included in this repository to avoid exceeding GitHub size limits. The primary model used by MediaVault, models/deepseek-ocr.gguf, is expected to be downloaded separately and stored in the models/ folder.

- To simplify first-run setup, a helper PowerShell script is provided at scripts/download_model.ps1 which downloads the model from a hosted URL and optionally verifies its SHA256 checksum.

- If you maintain the model file in another storage location (S3, Google Drive, or GitHub Releases), host the direct download link there and pass it to the script below.

### Quick usage (PowerShell)

1. Create the models folder (if it doesn't exist):

`powershell
mkdir models -ErrorAction SilentlyContinue
`

2. Run the download helper (replace <MODEL_URL> and optional <SHA256>):

`powershell
.\scripts\download_model.ps1 -Url "<MODEL_URL>" -OutPath "models\\deepseek-ocr.gguf" -Sha256 "<optional-sha256>"
`

3. Confirm the file exists at models\\deepseek-ocr.gguf before launching the app.

If you want the project to host the model in-repo, consider using Git LFS or GitHub Releases; otherwise keep the model external and use this script during setup.

### Removing Large Files From Git History

If large files were committed earlier and you need them removed from the repository history, see scripts/remove_large_history.md for safe, step-by-step instructions using git-filter-repo or the BFG Repo-Cleaner. Rewriting history is destructive for shared branches  read that document carefully and notify collaborators before proceeding.

