"""
MediaVault Scanner - Database Module
Handles SQLite database operations for media metadata storage.
"""

import sqlite3
import os
from typing import Optional, List, Dict, Any
from contextlib import contextmanager


class MediaDatabase:
    """Manages the SQLite database for media metadata."""
    
    def __init__(self, db_path: str = "metadata.db"):
        """
        Initialize the database connection.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def init_database(self):
        """Create the database schema if it doesn't exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS media_metadata (
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
                )
            """)

            # Create index on filepath for faster lookups
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_filepath
                ON media_metadata(filepath)
            """)

            # Add thumbnail_path column if it doesn't exist (for existing databases)
            try:
                cursor.execute("ALTER TABLE media_metadata ADD COLUMN thumbnail_path TEXT")
            except sqlite3.OperationalError:
                # Column already exists
                pass
    
    def file_exists(self, filepath: str) -> bool:
        """
        Check if a file already exists in the database.
        
        Args:
            filepath: Full path to the file
            
        Returns:
            True if file exists in database, False otherwise
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM media_metadata WHERE filepath = ?",
                (filepath,)
            )
            count = cursor.fetchone()[0]
            return count > 0
    
    def insert_metadata(self, metadata: Dict[str, Any]) -> bool:
        """
        Insert or update media metadata in the database.

        Args:
            metadata: Dictionary containing metadata fields

        Returns:
            True if successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO media_metadata (
                        filepath, filename, file_type, date_time_original,
                        gps_latitude, gps_longitude, person_count,
                        ocr_text_summary, object_keywords, emotion_sentiment,
                        thumbnail_path
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    metadata.get('filepath'),
                    metadata.get('filename'),
                    metadata.get('file_type'),
                    metadata.get('date_time_original'),
                    metadata.get('gps_latitude'),
                    metadata.get('gps_longitude'),
                    metadata.get('person_count'),
                    metadata.get('ocr_text_summary'),
                    metadata.get('object_keywords'),
                    metadata.get('emotion_sentiment'),
                    metadata.get('thumbnail_path')
                ))
                return True
        except Exception as e:
            print(f"Database insert error: {e}")
            return False
    
    def get_all_metadata(self) -> List[Dict[str, Any]]:
        """
        Retrieve all metadata records from the database.
        
        Returns:
            List of dictionaries containing metadata records
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM media_metadata ORDER BY id DESC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def get_metadata_by_filepath(self, filepath: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve metadata for a specific file.
        
        Args:
            filepath: Full path to the file
            
        Returns:
            Dictionary containing metadata or None if not found
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM media_metadata WHERE filepath = ?",
                (filepath,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_record_count(self) -> int:
        """Get the total number of records in the database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM media_metadata")
            return cursor.fetchone()[0]

    def get_analytics_summary(self) -> Dict[str, Any]:
        """
        Get analytics summary for the dashboard.

        Returns:
            Dictionary containing analytics data
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Total counts
            cursor.execute("SELECT COUNT(*) FROM media_metadata WHERE file_type LIKE 'image%'")
            image_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM media_metadata WHERE file_type LIKE 'video%'")
            video_count = cursor.fetchone()[0]

            # Geographic distribution
            cursor.execute("""
                SELECT COUNT(DISTINCT gps_latitude || ',' || gps_longitude)
                FROM media_metadata
                WHERE gps_latitude IS NOT NULL AND gps_longitude IS NOT NULL
            """)
            unique_locations = cursor.fetchone()[0]

            # Average people per photo
            cursor.execute("""
                SELECT AVG(person_count)
                FROM media_metadata
                WHERE person_count IS NOT NULL AND person_count > 0
            """)
            avg_people = cursor.fetchone()[0] or 0

            # Emotion sentiment distribution
            cursor.execute("""
                SELECT emotion_sentiment, COUNT(*) as count
                FROM media_metadata
                WHERE emotion_sentiment IS NOT NULL
                GROUP BY emotion_sentiment
                ORDER BY count DESC
            """)
            emotion_distribution = dict(cursor.fetchall())

            # Top OCR keywords
            cursor.execute("""
                SELECT object_keywords
                FROM media_metadata
                WHERE object_keywords IS NOT NULL AND object_keywords != ''
            """)
            all_keywords = []
            for row in cursor.fetchall():
                keywords = row[0].split(',')
                all_keywords.extend([k.strip() for k in keywords if k.strip()])

            # Count keyword frequency
            keyword_counts = {}
            for keyword in all_keywords:
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1

            # Get top 3 keywords
            top_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:3]

            return {
                'total_files': image_count + video_count,
                'image_count': image_count,
                'video_count': video_count,
                'unique_locations': unique_locations,
                'avg_people_per_photo': round(avg_people, 2),
                'emotion_distribution': emotion_distribution,
                'top_keywords': [k[0] for k in top_keywords]
            }

    def get_filtered_metadata(self,
                             emotion_filter: Optional[str] = None,
                             person_count_min: Optional[int] = None,
                             person_count_max: Optional[int] = None,
                             keyword_search: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get filtered metadata records.

        Args:
            emotion_filter: Filter by emotion sentiment
            person_count_min: Minimum person count
            person_count_max: Maximum person count
            keyword_search: Search in object keywords

        Returns:
            List of filtered metadata records
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            query = "SELECT * FROM media_metadata WHERE 1=1"
            params = []

            if emotion_filter and emotion_filter != "All":
                query += " AND emotion_sentiment = ?"
                params.append(emotion_filter)

            if person_count_min is not None:
                query += " AND person_count >= ?"
                params.append(person_count_min)

            if person_count_max is not None:
                query += " AND person_count <= ?"
                params.append(person_count_max)

            if keyword_search:
                query += " AND object_keywords LIKE ?"
                params.append(f"%{keyword_search}%")

            query += " ORDER BY id DESC"

            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def export_to_csv(self, filepath: str, records: Optional[List[Dict[str, Any]]] = None) -> bool:
        """
        Export metadata to CSV file.

        Args:
            filepath: Path to save the CSV file
            records: Optional list of records to export (if None, exports all)

        Returns:
            True if successful, False otherwise
        """
        import csv

        try:
            if records is None:
                records = self.get_all_metadata()

            if not records:
                return False

            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'id', 'filepath', 'filename', 'file_type', 'date_time_original',
                    'gps_latitude', 'gps_longitude', 'person_count',
                    'ocr_text_summary', 'object_keywords', 'emotion_sentiment'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for record in records:
                    writer.writerow(record)

            return True
        except Exception as e:
            print(f"CSV export error: {e}")
            return False

