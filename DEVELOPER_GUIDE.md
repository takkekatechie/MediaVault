# MediaVault Scanner - Developer Guide

## 🛠️ Development Setup

### Prerequisites
- Python 3.10 or higher
- Git
- Windows 10/11 (for testing Windows-specific features)
- Tesseract OCR installed

### Initial Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/MediaVault.git
cd MediaVault

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Add to PATH or configure in the app
```

---

## 📁 Project Structure

```
MediaVault/
├── main.py                 # Entry point, GUI application
├── database.py             # SQLite database operations
├── metadata_extractor.py   # Core extraction logic
├── scanner.py              # File scanning coordinator
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── mediavault.spec         # PyInstaller specification
├── build.py                # Build automation script
├── test_extraction.py      # Testing utilities
└── docs/                   # Documentation
    ├── README.md
    ├── QUICKSTART.md
    ├── PROJECT_SUMMARY.md
    └── DEVELOPER_GUIDE.md
```

---

## 🏗️ Architecture Overview

### Module Responsibilities

#### `main.py` - GUI Application
- CustomTkinter-based user interface
- Event handling and user interactions
- Threading for non-blocking scans
- Tesseract setup dialog

**Key Classes**:
- `MediaVaultApp`: Main application window
- `TesseractSetupDialog`: Tesseract configuration dialog

#### `database.py` - Data Persistence
- SQLite database management
- CRUD operations for media metadata
- Connection pooling via context managers

**Key Classes**:
- `MediaDatabase`: Database interface

**Key Methods**:
- `init_database()`: Create schema
- `insert_metadata()`: Insert/update records
- `file_exists()`: Check for duplicates
- `get_all_metadata()`: Retrieve all records

#### `metadata_extractor.py` - Extraction Engine
- EXIF data extraction
- GPS coordinate conversion
- Face detection using OpenCV
- OCR text extraction
- Emotion/sentiment heuristics

**Key Classes**:
- `MetadataExtractor`: Main extraction engine

**Key Methods**:
- `extract_metadata()`: Main extraction orchestrator
- `_extract_exif_data()`: EXIF and GPS extraction
- `_detect_faces_image()`: Face detection for images
- `_extract_ocr_text()`: OCR processing
- `_analyze_emotion_sentiment()`: Heuristic analysis

#### `scanner.py` - Scan Coordinator
- Recursive directory traversal
- Progress tracking
- Coordination between extraction and database

**Key Classes**:
- `MediaScanner`: Scan orchestrator

**Key Methods**:
- `scan_directory()`: Main scan loop
- `_find_media_files()`: Recursive file discovery
- `stop_scan()`: Graceful scan termination

#### `config.py` - Configuration
- Application settings
- Tesseract path management
- User preferences persistence

**Key Classes**:
- `Config`: Configuration manager (static class)

---

## 🔧 Extending the Application

### Adding New Metadata Fields

1. **Update Database Schema** (`database.py`):
```python
# In init_database() method
cursor.execute("""
    CREATE TABLE IF NOT EXISTS media_metadata (
        ...
        your_new_field TEXT,  -- Add your field here
        ...
    )
""")
```

2. **Update Extraction Logic** (`metadata_extractor.py`):
```python
# In extract_metadata() method
metadata = {
    ...
    'your_new_field': self._extract_your_data(filepath),
    ...
}

# Add extraction method
def _extract_your_data(self, filepath: str) -> str:
    # Your extraction logic here
    return extracted_value
```

3. **Update Database Insert** (`database.py`):
```python
# In insert_metadata() method
cursor.execute("""
    INSERT OR REPLACE INTO media_metadata (
        ..., your_new_field
    ) VALUES (..., ?)
""", (..., metadata.get('your_new_field')))
```

4. **Update UI Display** (`main.py`):
```python
# In _create_data_row() method
# Add new column to display your field
```

### Adding New File Type Support

1. **Update Constants** (`metadata_extractor.py`):
```python
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.heic', '.your_ext'}
```

2. **Add Type-Specific Extraction**:
```python
def _extract_your_type_metadata(self, filepath: str, metadata: Dict):
    # Type-specific extraction logic
    pass
```

### Customizing the UI Theme

Edit `config.py`:
```python
APPEARANCE_MODE = "dark"  # "dark", "light", or "system"
COLOR_THEME = "blue"      # "blue", "green", or "dark-blue"
```

Or create custom color theme in `main.py`:
```python
ctk.set_default_color_theme("path/to/custom_theme.json")
```

---

## 🧪 Testing

### Running Tests
```bash
# Test database operations
python test_extraction.py

# Test single file extraction
python test_extraction.py path/to/test/image.jpg
```

### Manual Testing Checklist
- [ ] Directory selection and browsing
- [ ] Scan start/stop functionality
- [ ] Progress bar updates
- [ ] Face detection on various images
- [ ] OCR on images with text
- [ ] GPS coordinate extraction
- [ ] Emotion heuristic classification
- [ ] Database persistence
- [ ] Update existing records option
- [ ] Tesseract path configuration

### Creating Test Data
```python
# Create test metadata
test_data = {
    'filepath': 'C:\\test\\sample.jpg',
    'filename': 'sample.jpg',
    'file_type': 'Image',
    # ... other fields
}

# Insert into database
db = MediaDatabase()
db.insert_metadata(test_data)
```

---

## 📦 Building and Distribution

### Development Build
```bash
# Quick build for testing
pyinstaller main.py
```

### Production Build
```bash
# Using the build script (recommended)
python build.py

# Or manually with spec file
pyinstaller mediavault.spec
```

### Build Configuration
Edit `mediavault.spec` to customize:
- Executable name
- Icon file
- Hidden imports
- Data files to include
- Console vs windowed mode

---

## 🐛 Debugging

### Enable Console Output
In `mediavault.spec`, change:
```python
console=True,  # Shows console window for debugging
```

### Logging
Add logging throughout the code:
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

### Common Issues

**Issue**: Tesseract not found
- Check `Config.TESSERACT_PATH`
- Verify Tesseract installation
- Test with `pytesseract.get_tesseract_version()`

**Issue**: Face detection not working
- Verify Haar Cascade file is included
- Check OpenCV installation
- Test with simple image

**Issue**: Database locked
- Ensure only one instance is running
- Check file permissions
- Close all database connections properly

---

## 🚀 Performance Optimization

### Database Optimization
```python
# Add indexes for frequently queried fields
cursor.execute("CREATE INDEX idx_file_type ON media_metadata(file_type)")
cursor.execute("CREATE INDEX idx_date ON media_metadata(date_time_original)")
```

### Batch Processing
```python
# Process files in batches
batch_size = 100
for i in range(0, len(files), batch_size):
    batch = files[i:i+batch_size]
    # Process batch
```

### Caching
```python
# Cache face cascade classifier
@lru_cache(maxsize=1)
def get_face_cascade():
    return cv2.CascadeClassifier(cascade_path)
```

---

## 📚 Additional Resources

- [CustomTkinter Documentation](https://customtkinter.tomschimansky.com/)
- [OpenCV Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Tesseract OCR Documentation](https://tesseract-ocr.github.io/)
- [PyInstaller Manual](https://pyinstaller.org/en/stable/)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Document all public methods with docstrings
- Keep functions focused and single-purpose
- Use meaningful variable names

---

**Happy Coding! 🎉**

