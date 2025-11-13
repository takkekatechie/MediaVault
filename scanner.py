"""
MediaVault Scanner - File Scanner Module (Enhanced VL-OCR Version)
Recursively scans directories for media files and coordinates metadata extraction.
"""

import os
from pathlib import Path
from typing import List, Callable, Optional, Dict, Any
from database import MediaDatabase
from metadata_extractor import MetadataExtractor


class MediaScanner:
    """Scans directories for media files and extracts metadata."""

    # Supported file extensions
    SUPPORTED_EXTENSIONS = {
        '.jpg', '.jpeg', '.png', '.heic',  # Images
        '.mp4', '.mov', '.avi'              # Videos
    }

    def __init__(self, db_path: str = "metadata.db", gguf_ocr_config: Dict[str, Any] = None):
        """
        Initialize the media scanner.

        Args:
            db_path: Path to the SQLite database file
            gguf_ocr_config: Configuration dictionary for GGUF OCR engine
        """
        self.database = MediaDatabase(db_path)
        self.extractor = MetadataExtractor(gguf_ocr_config=gguf_ocr_config)
        self.should_stop = False
    
    def scan_directory(
        self,
        directory: str,
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
        update_existing: bool = False
    ) -> dict:
        """
        Recursively scan a directory for media files and extract metadata.
        
        Args:
            directory: Path to the directory to scan
            progress_callback: Optional callback function(current, total, filename)
            update_existing: If True, update existing files; if False, skip them
            
        Returns:
            Dictionary with scan statistics
        """
        self.should_stop = False
        
        # Find all media files
        media_files = self._find_media_files(directory)
        total_files = len(media_files)
        
        stats = {
            'total_found': total_files,
            'processed': 0,
            'skipped': 0,
            'errors': 0,
            'new_records': 0,
            'updated_records': 0
        }
        
        # Process each file
        for index, filepath in enumerate(media_files, start=1):
            if self.should_stop:
                break
            
            filename = os.path.basename(filepath)
            
            # Update progress
            if progress_callback:
                progress_callback(index, total_files, filename)
            
            try:
                # Check if file already exists in database
                file_exists = self.database.file_exists(filepath)
                
                if file_exists and not update_existing:
                    stats['skipped'] += 1
                    continue
                
                # Extract metadata
                metadata = self.extractor.extract_metadata(filepath)
                
                # Insert into database
                success = self.database.insert_metadata(metadata)
                
                if success:
                    stats['processed'] += 1
                    if file_exists:
                        stats['updated_records'] += 1
                    else:
                        stats['new_records'] += 1
                else:
                    stats['errors'] += 1
                    
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                stats['errors'] += 1
        
        return stats
    
    def _find_media_files(self, directory: str) -> List[str]:
        """
        Recursively find all media files in a directory.
        
        Args:
            directory: Path to the directory to scan
            
        Returns:
            List of full file paths
        """
        media_files = []
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_ext = Path(file).suffix.lower()
                    if file_ext in self.SUPPORTED_EXTENSIONS:
                        full_path = os.path.join(root, file)
                        media_files.append(full_path)
        except Exception as e:
            print(f"Error scanning directory: {e}")
        
        return media_files
    
    def stop_scan(self):
        """Signal the scanner to stop processing."""
        self.should_stop = True
    
    def get_database(self) -> MediaDatabase:
        """Get the database instance."""
        return self.database

