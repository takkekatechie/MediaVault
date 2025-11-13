# MediaVault Scanner - Project Summary

## 📋 Project Overview

**MediaVault Scanner** is a professional-grade, self-contained Python desktop application for Windows 10/11 that recursively scans local directories for image and video files, extracts comprehensive metadata, and stores it in a structured SQLite database.

---

## 🎯 Core Functionality

### 1. File Scanning
- Recursively scans user-specified directories
- Supports: `.jpg`, `.jpeg`, `.png`, `.heic`, `.mp4`, `.mov`, `.avi`
- Real-time progress tracking
- Idempotent operations (skip or update existing records)

### 2. Metadata Extraction

#### EXIF & GPS Data
- Extracts original timestamp from EXIF data
- Converts GPS coordinates to decimal format (latitude/longitude)
- Supports both PIL and exifread libraries for maximum compatibility

#### Face Detection
- Uses OpenCV Haar Cascade classifier
- Counts number of faces in images
- For videos: samples frame at 5-second mark

#### OCR Text Extraction
- Uses Tesseract OCR engine
- Extracts text from images and video frames
- Filters stopwords and extracts meaningful keywords
- Stores top 3-5 unique words as object keywords

#### Emotion/Sentiment Heuristic
- **Rule 1**: Keyword-based sentiment from filename/path
  - Positive: vacation, birthday, party, wedding, celebration, trip, holiday
  - Negative: funeral, work, meeting, office
- **Rule 2**: Time-of-day inference from EXIF timestamp
  - Daytime (6 AM - 6 PM) or Nighttime
- Output format: "Sentiment/Context" (e.g., "Positive/Vacation/Daytime")

### 3. Database Storage
- SQLite database (`metadata.db`)
- Structured schema with 11 fields
- Indexed for fast lookups
- Persistent, file-based storage

---

## 🏗️ Architecture

### File Structure
```
MediaVault/
├── main.py                 # Main GUI application
├── database.py             # Database operations
├── metadata_extractor.py   # Metadata extraction logic
├── scanner.py              # File scanning and coordination
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── mediavault.spec         # PyInstaller build specification
├── build.py                # Automated build script
├── test_extraction.py      # Testing utilities
├── README.md               # Full documentation
├── QUICKSTART.md           # Quick start guide
├── LICENSE                 # MIT License
└── .gitignore              # Git ignore rules
```

### Technology Stack
- **Language**: Python 3.10+
- **GUI**: CustomTkinter (modern, dark-mode interface)
- **Image Processing**: Pillow, exifread
- **OCR**: pytesseract (requires Tesseract installation)
- **Computer Vision**: opencv-python (face detection)
- **Database**: SQLite3 (built-in)
- **Packaging**: PyInstaller

---

## 🗄️ Database Schema

```sql
CREATE TABLE media_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filepath TEXT UNIQUE NOT NULL,
    filename TEXT,
    file_type TEXT,                -- 'Image' or 'Video'
    date_time_original TEXT,       -- EXIF timestamp
    gps_latitude REAL,             -- Decimal format
    gps_longitude REAL,            -- Decimal format
    person_count INTEGER,          -- Face detection count
    ocr_text_summary TEXT,         -- First 100 chars of OCR text
    object_keywords TEXT,          -- Comma-separated keywords
    emotion_sentiment TEXT         -- Heuristic classification
);
```

---

## 🎨 User Interface

### Layout
1. **Controls Panel** (Top)
   - Directory selection input
   - Browse button
   - Start/Stop scan button
   - Update existing records checkbox

2. **Data View Panel** (Center)
   - Scrollable table with columns:
     - Filename
     - Date/Time Original
     - Person Count
     - Summary
   - Displays up to 100 most recent records

3. **Status/Log Panel** (Bottom)
   - Progress bar
   - Real-time status messages
   - Scan statistics

### Features
- Modern dark-mode aesthetic
- Responsive layout
- Real-time progress updates
- Threaded scanning (non-blocking UI)

---

## 🚀 Deployment

### Building the Executable

**Method 1: Using the build script (Recommended)**
```bash
python build.py
```

**Method 2: Using PyInstaller directly**
```bash
pyinstaller mediavault.spec
```

**Method 3: Manual PyInstaller command**
```bash
pyinstaller --name=MediaVaultScanner --onefile --windowed main.py
```

### Distribution Requirements
1. **Executable**: `MediaVaultScanner.exe` (in `dist/` folder)
2. **Documentation**: Include `README.md` and `QUICKSTART.md`
3. **Tesseract**: Users must install separately (NOT bundled)

---

## ⚙️ Configuration

### Tesseract Setup
The application requires Tesseract OCR for text extraction:

1. **Auto-detection**: Checks common installation paths and system PATH
2. **Manual configuration**: Users can specify path via setup dialog
3. **Persistent storage**: Path saved in `mediavault_config.json`

### Configuration File
`mediavault_config.json` stores:
- Tesseract installation path
- Appearance mode (dark/light/system)
- Color theme

---

## 🧪 Testing

### Manual Testing
```bash
# Test metadata extraction on a single file
python test_extraction.py path/to/image.jpg

# Test database operations
python test_extraction.py
```

### Test Coverage
- Database CRUD operations
- Metadata extraction from images
- Metadata extraction from videos
- GPS coordinate conversion
- Face detection
- OCR text extraction
- Emotion heuristic logic

---

## 📦 Dependencies

### Required Python Packages
- `customtkinter>=5.2.0` - Modern GUI framework
- `Pillow>=10.0.0` - Image processing
- `exifread>=3.0.0` - EXIF data extraction
- `pytesseract>=0.3.10` - OCR wrapper
- `opencv-python>=4.8.0` - Computer vision
- `numpy>=1.24.0` - Numerical operations
- `pyinstaller>=6.0.0` - Executable packaging

### External Dependencies
- **Tesseract OCR**: Must be installed separately by end users
  - Download: https://github.com/UB-Mannheim/tesseract/wiki
  - Installation path: `C:\Program Files\Tesseract-OCR`

---

## 🔒 Security & Privacy

- **100% Local Processing**: No cloud services or external APIs
- **No Data Transmission**: All data stays on the user's machine
- **File-based Storage**: SQLite database stored locally
- **No Telemetry**: No usage tracking or analytics

---

## 🎓 Key Implementation Details

### Idempotency
- Checks if filepath exists in database before processing
- Option to skip or update existing records
- Prevents duplicate processing

### Threading
- Scanning runs in background thread
- UI remains responsive during long scans
- Progress updates via callback mechanism

### Error Handling
- Graceful degradation if metadata extraction fails
- Continues processing remaining files on errors
- Detailed error logging in status panel

### Performance Considerations
- Face detection: CPU-intensive, may be slow on large datasets
- OCR: Requires Tesseract, adds processing time
- Database: Indexed for fast lookups
- UI: Limits display to 100 records for performance

---

## 📈 Future Enhancement Possibilities

- Export to CSV/JSON
- Advanced search and filtering
- Thumbnail preview
- Batch editing of metadata
- Cloud backup integration
- Machine learning-based emotion detection
- Multi-language OCR support
- Video timeline analysis

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👥 Target Users

- Photographers organizing large photo collections
- Content creators managing media libraries
- Researchers analyzing image datasets
- Anyone needing to catalog and search local media files

---

**Project Status**: ✅ Complete and ready for deployment
**Last Updated**: 2025-01-15

