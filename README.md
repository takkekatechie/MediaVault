# MediaVault Scanner

**A Professional-Grade Local Photo/Video Metadata Repository for Windows**

MediaVault Scanner is a complete, self-contained Python desktop application designed to recursively scan local directories for image and video files, extract comprehensive metadata (including EXIF data, GPS coordinates, face detection, OCR text, and emotion heuristics), and persist this information into a structured SQLite database.

---

## 🎯 Features

### Scanning & Metadata Extraction
- **Recursive Directory Scanning**: Automatically finds all supported media files in a directory tree
- **Deep Metadata Extraction**:
  - EXIF data (timestamps, camera settings)
  - GPS coordinates (latitude/longitude in decimal format)
  - Face detection (person count using OpenCV)
  - OCR text extraction (using Tesseract)
  - Object keywords identification
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

- **Operating System**: Windows 10 or Windows 11
- **Python**: 3.10 or higher (for development)
- **Tesseract OCR**: Required for text extraction (see installation below)

---

## 📦 Installation

### Option 1: Using the Pre-built Executable (Recommended for End Users)

1. Download the latest `MediaVaultScanner.exe` from the releases page
2. Install Tesseract OCR (see instructions below)
3. Run `MediaVaultScanner.exe`

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

4. **Install Tesseract OCR** (see detailed instructions below)

5. **Run the application**:
   ```bash
   python main.py
   ```

---

## 🔍 Tesseract OCR Installation (CRITICAL REQUIREMENT)

MediaVault Scanner requires Tesseract OCR to extract text from images and videos. Follow these steps carefully:

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

### Scanning Media Files

1. **Launch the application**:
   - Run `MediaVaultScanner.exe` (executable) or `python main.py` (source)

2. **Select a target directory**:
   - Click the **"Browse"** button
   - Choose the folder containing your photos and videos

3. **Configure scan options** (optional):
   - Check **"Update existing records"** to re-scan previously processed files

4. **Start scanning**:
   - Click **"Start Scan"**
   - Monitor progress in real-time
   - View results in the data table

5. **Stop scanning** (optional):
   - Click **"Stop Scan"** to halt the process
   - Automatically transitions to Analysis Dashboard

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
- `ocr_text_summary`: Extracted OCR text
- `object_keywords`: Comma-separated keywords
- `emotion_sentiment`: Emotion/sentiment classification
- `thumbnail_path`: Path to 64x64 thumbnail image (NEW!)

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

1. **Tesseract is NOT bundled**: Users must install Tesseract separately
2. **Test the executable**: Always test on a clean Windows machine
3. **Include README**: Distribute the README with installation instructions

---

## 🛠️ Technology Stack

- **Language**: Python 3.10+
- **GUI Framework**: CustomTkinter (modern, dark-mode UI)
- **Image Processing**: Pillow (PIL), exifread
- **OCR**: pytesseract
- **Computer Vision**: opencv-python (face detection)
- **Database**: SQLite3 (built-in)
- **Packaging**: PyInstaller

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## ⚠️ Troubleshooting

### Tesseract Not Found Error

**Problem**: Application shows "Tesseract not found" warning

**Solution**:
- Verify Tesseract is installed at `C:\Program Files\Tesseract-OCR`
- Check that Tesseract is in your system PATH
- Try manually specifying the path in the setup dialog
- Restart the application after making changes

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
