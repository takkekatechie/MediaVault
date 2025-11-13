# MediaVault Scanner - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### For End Users (Using the Executable)

1. **Download the Application**
   - Get `MediaVaultScanner.exe` from the releases page

2. **Install Tesseract OCR** (One-time setup)
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Install to default location: `C:\Program Files\Tesseract-OCR`
   - Add to Windows PATH (see detailed instructions in README.md)
   - **OR** specify the path manually when prompted by the app

3. **Run the Application**
   - Double-click `MediaVaultScanner.exe`
   - If Tesseract is not found, follow the on-screen setup instructions

4. **Scan Your First Directory**
   - Click **"Browse"** and select a folder with photos/videos
   - Click **"Start Scan"**
   - Watch the progress and view results in the table

5. **Explore the Analysis Dashboard** (NEW!)
   - After scan completes, you'll see the Analysis Dashboard
   - Review key insights about your media collection
   - Filter data by emotion, person count, or keywords
   - Export results to CSV for further analysis

---

### For Developers (Running from Source)

1. **Setup Environment**
   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/MediaVault.git
   cd MediaVault

   # Create virtual environment
   python -m venv venv
   venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Install Tesseract OCR**
   - Follow the same instructions as end users above

3. **Run the Application**
   ```bash
   python main.py
   ```

4. **Build the Executable** (Optional)
   ```bash
   # Using the spec file
   pyinstaller mediavault.spec

   # Or use the build script
   python build.py

   # Executable will be in dist/MediaVaultScanner.exe
   ```

---

## 📊 What Gets Extracted?

For each image or video file, MediaVault extracts:

- ✅ **Filename and path**
- ✅ **File type** (Image or Video)
- ✅ **Date/Time Original** (from EXIF)
- ✅ **GPS Coordinates** (latitude/longitude)
- ✅ **Person Count** (face detection)
- ✅ **OCR Text** (extracted text from images)
- ✅ **Object Keywords** (meaningful words found)
- ✅ **Emotion/Sentiment** (heuristic based on context)

---

## 🎯 Tips for Best Results

### Face Detection
- Works best with clear, front-facing photos
- Requires sufficient image resolution
- For videos, only the frame at 5 seconds is analyzed

### OCR Text Extraction
- Requires clear, readable text in images
- Works better with high-contrast text
- Tesseract must be properly installed

### GPS Coordinates
- Only available if the camera/phone recorded GPS data
- Check your device's location settings

### Emotion/Sentiment Analysis
- Based on folder names (e.g., "Vacation", "Birthday")
- Time of day (Daytime vs Nighttime)
- Simple heuristic, not AI-based emotion detection

---

## 🔧 Common Issues

**Q: "Tesseract not found" error**
- A: Install Tesseract and add it to your Windows PATH, or specify the path manually

**Q: No faces detected in my photos**
- A: Face detection works best on clear, front-facing photos with good lighting

**Q: Scan is very slow**
- A: OCR and face detection are CPU-intensive. Scanning large directories takes time.

**Q: Can I scan the same folder twice?**
- A: Yes! Check "Update existing records" to re-scan files, or leave unchecked to skip them.

**Q: How do I access the Analysis Dashboard?**
- A: It appears automatically after a scan completes or when you click "Stop Scan". You can also click "← Back to Scan" to return.

**Q: Can I export only certain records?**
- A: Yes! Use the filters (emotion, person count, keywords) to narrow down your data, then choose "Export Filtered Records Only".

---

## 📁 Where is My Data Stored?

- **Database**: `metadata.db` (in the same folder as the application)
- **Configuration**: `mediavault_config.json` (stores Tesseract path and preferences)

You can open `metadata.db` with any SQLite browser to query your data directly.

---

## 🆘 Need Help?

- Read the full [README.md](README.md) for detailed documentation
- Check the [Troubleshooting](README.md#-troubleshooting) section
- Open an issue on GitHub

---

**Happy Scanning! 📸🎥**

