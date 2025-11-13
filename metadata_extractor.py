"""
MediaVault Scanner - Metadata Extraction Module
Extracts metadata from images and videos using various techniques.
"""

import os
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from pathlib import Path

# Image processing
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import exifread

# OCR
import pytesseract

# Computer Vision
import cv2
import numpy as np


class MetadataExtractor:
    """Extracts comprehensive metadata from media files."""

    # Supported file extensions
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.heic'}
    VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi'}

    # Sentiment keywords for heuristic analysis
    POSITIVE_KEYWORDS = {'vacation', 'birthday', 'party', 'wedding', 'celebration', 'trip', 'holiday'}
    NEGATIVE_KEYWORDS = {'funeral', 'work', 'meeting', 'office'}

    # Common stopwords to filter from OCR
    STOPWORDS = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'is', 'are', 'was', 'were'}

    # Object/scene detection thresholds (simplified local heuristic)
    # Note: This is a basic color/pattern-based heuristic, not ML-based detection
    COLOR_RANGES = {
        'sky': {'lower': (90, 50, 50), 'upper': (130, 255, 255)},      # Blue hues
        'grass': {'lower': (35, 40, 40), 'upper': (85, 255, 255)},     # Green hues
        'water': {'lower': (85, 50, 50), 'upper': (125, 255, 255)},    # Cyan/blue hues
        'sunset': {'lower': (0, 100, 100), 'upper': (25, 255, 255)},   # Orange/red hues
        'foliage': {'lower': (25, 30, 30), 'upper': (95, 255, 255)},   # Green/yellow hues
    }

    # Thumbnail settings
    THUMBNAIL_SIZE = (64, 64)
    THUMBNAIL_DIR = "thumbnails"

    def __init__(self):
        """Initialize the metadata extractor with face detection cascade."""
        # Load Haar Cascade for face detection
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

        # Create thumbnails directory if it doesn't exist
        os.makedirs(self.THUMBNAIL_DIR, exist_ok=True)
    
    def extract_metadata(self, filepath: str) -> Dict[str, Any]:
        """
        Extract all metadata from a media file.
        
        Args:
            filepath: Full path to the media file
            
        Returns:
            Dictionary containing all extracted metadata
        """
        file_ext = Path(filepath).suffix.lower()
        filename = os.path.basename(filepath)
        
        # Determine file type
        if file_ext in self.IMAGE_EXTENSIONS:
            file_type = 'Image'
        elif file_ext in self.VIDEO_EXTENSIONS:
            file_type = 'Video'
        else:
            file_type = 'Unknown'
        
        # Initialize metadata dictionary
        metadata = {
            'filepath': filepath,
            'filename': filename,
            'file_type': file_type,
            'date_time_original': None,
            'gps_latitude': None,
            'gps_longitude': None,
            'person_count': 0,
            'ocr_text_summary': '',
            'object_keywords': '',
            'emotion_sentiment': 'Neutral',
            'thumbnail_path': None
        }

        try:
            if file_type == 'Image':
                self._extract_image_metadata(filepath, metadata)
            elif file_type == 'Video':
                self._extract_video_metadata(filepath, metadata)

            # Apply emotion/sentiment heuristic
            metadata['emotion_sentiment'] = self._analyze_emotion_sentiment(filepath, metadata)

            # Generate thumbnail
            metadata['thumbnail_path'] = self._generate_thumbnail(filepath, file_type)

        except Exception as e:
            print(f"Error extracting metadata from {filename}: {e}")

        return metadata
    
    def _extract_image_metadata(self, filepath: str, metadata: Dict[str, Any]):
        """Extract metadata specific to image files."""
        # Extract EXIF data
        self._extract_exif_data(filepath, metadata)

        # Detect faces
        metadata['person_count'] = self._detect_faces_image(filepath)

        # Perform OCR
        ocr_text, ocr_keywords = self._extract_ocr_text(filepath)
        metadata['ocr_text_summary'] = ocr_text

        # Detect objects/scenes (local heuristic)
        object_tags = self._detect_objects_image(filepath)

        # Combine object tags and OCR keywords
        metadata['object_keywords'] = self._combine_keywords(object_tags, ocr_keywords)
    
    def _extract_video_metadata(self, filepath: str, metadata: Dict[str, Any]):
        """Extract metadata specific to video files."""
        # Sample a frame from the video (at 5 seconds)
        frame = self._sample_video_frame(filepath, at_second=5)

        if frame is not None:
            # Detect faces in the sampled frame
            metadata['person_count'] = self._detect_faces_frame(frame)

            # Perform OCR on the sampled frame
            ocr_text, ocr_keywords = self._extract_ocr_from_frame(frame)
            metadata['ocr_text_summary'] = ocr_text

            # Detect objects/scenes in the sampled frame (local heuristic)
            object_tags = self._detect_objects_frame(frame)

            # Combine object tags and OCR keywords
            metadata['object_keywords'] = self._combine_keywords(object_tags, ocr_keywords)
    
    def _extract_exif_data(self, filepath: str, metadata: Dict[str, Any]):
        """Extract EXIF data including timestamp and GPS coordinates."""
        try:
            # Try with PIL first
            with Image.open(filepath) as img:
                exif_data = img._getexif()
                if exif_data:
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        
                        # Extract datetime
                        if tag == 'DateTimeOriginal':
                            metadata['date_time_original'] = str(value)
                        
                        # Extract GPS data
                        elif tag == 'GPSInfo':
                            gps_lat, gps_lon = self._parse_gps_info(value)
                            metadata['gps_latitude'] = gps_lat
                            metadata['gps_longitude'] = gps_lon
        except Exception as e:
            # Fallback to exifread
            try:
                with open(filepath, 'rb') as f:
                    tags = exifread.process_file(f)
                    
                    # Extract datetime
                    if 'EXIF DateTimeOriginal' in tags:
                        metadata['date_time_original'] = str(tags['EXIF DateTimeOriginal'])
                    
                    # Extract GPS
                    if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
                        lat = self._convert_gps_to_decimal(
                            tags['GPS GPSLatitude'],
                            tags.get('GPS GPSLatitudeRef', 'N')
                        )
                        lon = self._convert_gps_to_decimal(
                            tags['GPS GPSLongitude'],
                            tags.get('GPS GPSLongitudeRef', 'E')
                        )
                        metadata['gps_latitude'] = lat
                        metadata['gps_longitude'] = lon
            except Exception as e2:
                pass

    def _parse_gps_info(self, gps_info: Dict) -> Tuple[Optional[float], Optional[float]]:
        """Parse GPS info from PIL EXIF data."""
        try:
            gps_latitude = gps_info.get(2)
            gps_latitude_ref = gps_info.get(1, 'N')
            gps_longitude = gps_info.get(4)
            gps_longitude_ref = gps_info.get(3, 'E')

            if gps_latitude and gps_longitude:
                lat = self._convert_gps_coords(gps_latitude, gps_latitude_ref)
                lon = self._convert_gps_coords(gps_longitude, gps_longitude_ref)
                return lat, lon
        except Exception:
            pass
        return None, None

    def _convert_gps_coords(self, coords, ref) -> float:
        """Convert GPS coordinates to decimal format."""
        decimal = coords[0] + coords[1] / 60 + coords[2] / 3600
        if ref in ['S', 'W']:
            decimal = -decimal
        return decimal

    def _convert_gps_to_decimal(self, coord, ref) -> Optional[float]:
        """Convert exifread GPS coordinate to decimal format."""
        try:
            degrees = float(coord.values[0].num) / float(coord.values[0].den)
            minutes = float(coord.values[1].num) / float(coord.values[1].den)
            seconds = float(coord.values[2].num) / float(coord.values[2].den)

            decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)

            if str(ref) in ['S', 'W']:
                decimal = -decimal

            return decimal
        except Exception:
            return None

    def _detect_faces_image(self, filepath: str) -> int:
        """Detect faces in an image file."""
        try:
            img = cv2.imread(filepath)
            if img is None:
                return 0
            return self._detect_faces_frame(img)
        except Exception:
            return 0

    def _detect_faces_frame(self, frame: np.ndarray) -> int:
        """Detect faces in a video frame or image array."""
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            return len(faces)
        except Exception:
            return 0

    def _sample_video_frame(self, filepath: str, at_second: int = 5) -> Optional[np.ndarray]:
        """Sample a single frame from a video file."""
        try:
            cap = cv2.VideoCapture(filepath)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_number = int(fps * at_second)

            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = cap.read()
            cap.release()

            return frame if ret else None
        except Exception:
            return None

    def _extract_ocr_text(self, filepath: str) -> Tuple[str, str]:
        """Extract text from an image using OCR."""
        try:
            img = Image.open(filepath)
            text = pytesseract.image_to_string(img)
            return self._process_ocr_text(text)
        except Exception:
            return '', ''

    def _extract_ocr_from_frame(self, frame: np.ndarray) -> Tuple[str, str]:
        """Extract text from a video frame using OCR."""
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_frame)
            text = pytesseract.image_to_string(pil_img)
            return self._process_ocr_text(text)
        except Exception:
            return '', ''

    def _process_ocr_text(self, text: str) -> Tuple[str, str]:
        """Process OCR text to extract summary and keywords."""
        if not text:
            return '', ''

        # Clean and tokenize
        words = text.lower().split()

        # Filter stopwords and short words
        meaningful_words = [
            word.strip('.,!?;:()[]{}"\'-')
            for word in words
            if len(word) > 2 and word.lower() not in self.STOPWORDS
        ]

        # Get unique words
        unique_words = []
        seen = set()
        for word in meaningful_words:
            if word not in seen and word.isalpha():
                unique_words.append(word)
                seen.add(word)
                if len(unique_words) >= 5:
                    break

        # Create summary (first 100 chars of original text)
        summary = text.strip()[:100]

        # Create keywords (top 3-5 unique words)
        keywords = ', '.join(unique_words[:5])

        return summary, keywords

    def _analyze_emotion_sentiment(self, filepath: str, metadata: Dict[str, Any]) -> str:
        """
        Apply rule-based heuristic for emotion/sentiment classification.

        Rules:
        1. Check filename and parent directory for sentiment keywords
        2. Infer time of day from date_time_original
        """
        sentiment = 'Neutral'
        context = ''

        # Rule 1: Keyword-based sentiment
        path_lower = filepath.lower()

        for keyword in self.POSITIVE_KEYWORDS:
            if keyword in path_lower:
                sentiment = 'Positive'
                context = keyword.capitalize()
                break

        if sentiment == 'Neutral':
            for keyword in self.NEGATIVE_KEYWORDS:
                if keyword in path_lower:
                    sentiment = 'Negative'
                    context = keyword.capitalize()
                    break

        # Rule 2: Time-of-day inference
        if metadata.get('date_time_original'):
            try:
                # Parse datetime (format: "YYYY:MM:DD HH:MM:SS")
                dt_str = metadata['date_time_original']
                dt = datetime.strptime(dt_str, '%Y:%m:%d %H:%M:%S')
                hour = dt.hour

                if 6 <= hour < 18:
                    time_context = 'Daytime'
                else:
                    time_context = 'Nighttime'

                if context:
                    context = f"{context}/{time_context}"
                else:
                    context = time_context
            except Exception:
                pass

        # Format final sentiment
        if context:
            return f"{sentiment}/{context}"
        else:
            return sentiment

    def _generate_thumbnail(self, filepath: str, file_type: str) -> Optional[str]:
        """
        Generate a thumbnail for the media file.

        Args:
            filepath: Full path to the media file
            file_type: Type of file ('Image' or 'Video')

        Returns:
            Path to the generated thumbnail, or None if failed
        """
        try:
            # Create a unique thumbnail filename based on the original file
            file_hash = str(hash(filepath))[-10:]  # Use last 10 digits of hash
            thumbnail_filename = f"thumb_{file_hash}.jpg"
            thumbnail_path = os.path.join(self.THUMBNAIL_DIR, thumbnail_filename)

            # Skip if thumbnail already exists
            if os.path.exists(thumbnail_path):
                return thumbnail_path

            if file_type == 'Image':
                # Generate thumbnail from image
                with Image.open(filepath) as img:
                    # Convert to RGB if necessary (for PNG with transparency, etc.)
                    if img.mode != 'RGB':
                        img = img.convert('RGB')

                    # Create thumbnail with exact size (crop to square if needed)
                    # First, resize maintaining aspect ratio
                    img.thumbnail((128, 128), Image.Resampling.LANCZOS)

                    # Create a square thumbnail by cropping/padding
                    thumb = Image.new('RGB', self.THUMBNAIL_SIZE, (0, 0, 0))

                    # Calculate position to paste (center the image)
                    paste_x = (self.THUMBNAIL_SIZE[0] - img.width) // 2
                    paste_y = (self.THUMBNAIL_SIZE[1] - img.height) // 2

                    thumb.paste(img, (paste_x, paste_y))
                    thumb.save(thumbnail_path, 'JPEG', quality=85)

            elif file_type == 'Video':
                # Generate thumbnail from video frame at 5 seconds
                cap = cv2.VideoCapture(filepath)

                # Set position to 5 seconds (5000 milliseconds)
                cap.set(cv2.CAP_PROP_POS_MSEC, 5000)

                # Read the frame
                success, frame = cap.read()
                cap.release()

                if success:
                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # Create PIL Image from frame
                    img = Image.fromarray(frame_rgb)

                    # Create thumbnail with exact size
                    img.thumbnail((128, 128), Image.Resampling.LANCZOS)

                    # Create a square thumbnail by cropping/padding
                    thumb = Image.new('RGB', self.THUMBNAIL_SIZE, (0, 0, 0))

                    # Calculate position to paste (center the image)
                    paste_x = (self.THUMBNAIL_SIZE[0] - img.width) // 2
                    paste_y = (self.THUMBNAIL_SIZE[1] - img.height) // 2

                    thumb.paste(img, (paste_x, paste_y))
                    thumb.save(thumbnail_path, 'JPEG', quality=85)
                else:
                    return None

            return thumbnail_path

        except Exception as e:
            print(f"Error generating thumbnail for {filepath}: {e}")
            return None

