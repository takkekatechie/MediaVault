# MediaVault Scanner - Analysis & Export Features

## 🎉 New Features Overview

MediaVault Scanner now includes a comprehensive **Analysis & Export Dashboard** that automatically appears after scan completion, providing powerful data visualization, filtering, and export capabilities.

---

## 📊 Analysis Dashboard

### Automatic Transition
- **After Scan Completion**: Automatically transitions to the Analysis Dashboard when a scan finishes
- **Manual Stop**: Clicking "Stop Scan" also transitions to the Analysis Dashboard
- **Easy Navigation**: "← Back to Scan" button returns to the scanning interface

### Key Insights Panel

The dashboard displays real-time analytics calculated from your scanned media:

#### 1. Total Files Scanned
- **Total count** of all media files in the database
- **Breakdown** by type: Images vs Videos
- Example: "150 files (Images: 120 | Videos: 30)"

#### 2. Geographic Distribution Summary
- **Unique GPS locations** detected across all files
- Based on distinct latitude/longitude coordinates
- Example: "42 unique locations"

#### 3. Average People Per Photo
- **Average person count** calculated from face detection
- Only includes photos where faces were detected
- Rounded to 1 decimal place
- Example: "2.3 people"

#### 4. Dominant Emotion/Sentiment Classification
- **Most common emotion** across all classified files
- **Percentage** of files with that emotion
- Based on the emotion heuristic analysis
- Example: "Positive (55% of classified files)"

#### 5. Top 3 OCR Keywords
- **Most frequently detected** keywords from OCR text
- Extracted from the `object_keywords` field
- Comma-separated list
- Example: "vacation, beach, family"

---

## 🔍 Data Filtering

### Filter Controls

The dashboard provides three powerful filtering options:

#### 1. Emotion Filter
- **Dropdown menu** with options:
  - All (no filter)
  - Positive
  - Neutral
  - Negative
- Filters records by the `emotion_sentiment` field

#### 2. Person Count Range
- **Min/Max input fields** for person count
- Filter by number of detected faces
- Examples:
  - Min: 1 (photos with at least 1 person)
  - Max: 5 (photos with at most 5 people)
  - Min: 2, Max: 4 (photos with 2-4 people)

#### 3. Keyword Search
- **Text search box** for keywords
- Searches within the `object_keywords` field
- Case-insensitive partial matching
- Example: Searching "beach" finds all records with "beach" in keywords

### Applying Filters
- Click **"Apply Filters"** button to update the data table
- Filters work **in combination** (AND logic)
- Table updates in **real-time** with filtered results
- Displays up to **100 records** for performance

### Interactive Data Table (NEW!)

The table displays 6 columns with full interactivity:

1. **Preview** (NEW!) - 64x64 pixel thumbnail
   - For images: Thumbnail of the actual image
   - For videos: Frame captured at 5-second mark
   - Click to open the file in default viewer

2. **Filename** (truncated to 25 characters)
   - Click to open the file in default viewer

3. **Date/Time** (from EXIF data)
   - Click to open the file in default viewer

4. **People** (person count from face detection)
   - Click to open the file in default viewer

5. **Emotion** (sentiment classification)
   - Click to open the file in default viewer

6. **Keywords** (OCR keywords, truncated to 30 characters)
   - Click to open the file in default viewer

**Interactive Features:**
- **Click any thumbnail** to open the original media file
- **Click any row** to open the original media file
- Files open in Windows default viewer/player (Photos app, VLC, etc.)
- Hover over rows to see hand cursor indicating clickability

---

## 📤 CSV Export Functionality

### Export Button
- Prominent **"📊 Export Data"** button in the top-right corner
- Available at all times in the Analysis Dashboard

### Export Options Dialog

When you click Export, a dialog appears with two choices:

#### 1. Export All Records
- Exports **every record** in the database
- Includes all 11 metadata fields
- Ignores current filters

#### 2. Export Filtered Records Only
- Exports **only the currently filtered** records
- Based on active emotion, person count, and keyword filters
- Useful for exporting specific subsets

### File Selection
- **File dialog** opens to choose save location
- Default extension: `.csv`
- User can specify custom filename

### CSV Format

The exported CSV includes all 11 fields:
1. `id` - Database record ID
2. `filepath` - Full path to the media file
3. `filename` - File name only
4. `file_type` - "image/jpeg", "video/mp4", etc.
5. `date_time_original` - EXIF timestamp
6. `gps_latitude` - Decimal latitude
7. `gps_longitude` - Decimal longitude
8. `person_count` - Number of detected faces
9. `ocr_text_summary` - Extracted OCR text
10. `object_keywords` - Comma-separated keywords
11. `emotion_sentiment` - Sentiment classification

### Success Confirmation
- **Success dialog** shows number of exported records and file path
- **Error dialog** appears if export fails

---

## 🎯 Usage Workflow

### Typical Analysis Workflow

1. **Complete a scan** (or stop an in-progress scan)
2. **Review the Key Insights** panel to understand your collection
3. **Apply filters** to narrow down specific types of media:
   - Find all "Positive" vacation photos
   - Find photos with 3+ people
   - Find images containing specific keywords
4. **Review filtered results** in the data table
5. **Export data**:
   - Export all for complete backup
   - Export filtered for specific analysis
6. **Return to scanning** to process more directories

---

## 💡 Use Cases

### Example 1: Finding Vacation Photos
1. Set Emotion filter to "Positive"
2. Search keywords for "vacation" or "beach"
3. Review filtered results
4. Export filtered records to CSV

### Example 2: Group Photos Analysis
1. Set Person Count Min to 3
2. Review photos with multiple people
3. Check geographic distribution
4. Export for further analysis

### Example 3: Complete Data Backup
1. Click "Export Data"
2. Choose "Export All Records"
3. Save to backup location
4. Open in Excel/Google Sheets for analysis

---

## 🔧 Technical Details

### Database Queries
- **Analytics**: Optimized SQL queries with aggregations
- **Filtering**: Dynamic WHERE clauses based on active filters
- **Performance**: Indexed queries for fast retrieval

### Real-time Updates
- Dashboard refreshes automatically when shown
- Filters apply instantly to in-memory data
- No database re-scanning required

### Data Integrity
- Export uses UTF-8 encoding for international characters
- CSV format compatible with Excel, Google Sheets, and data analysis tools
- All fields properly escaped for CSV format

---

## 📈 Future Enhancements

Potential future additions:
- Visual charts and graphs (bar charts, pie charts)
- Advanced search with multiple keyword combinations
- Date range filtering
- Export to JSON, XML formats
- Batch operations on filtered records
- Custom report generation

---

**The Analysis & Export Dashboard transforms MediaVault Scanner from a simple metadata extractor into a powerful media analysis tool!**

