
import unittest
from unittest.mock import MagicMock, patch
import os
import sys
import numpy as np

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from metadata_extractor import MetadataExtractor

class TestRawSupport(unittest.TestCase):
    def setUp(self):
        self.extractor = MetadataExtractor()

    def test_raw_extensions(self):
        self.assertIn('.arw', self.extractor.IMAGE_EXTENSIONS)
        self.assertIn('.cr2', self.extractor.IMAGE_EXTENSIONS)
        self.assertIn('.nef', self.extractor.IMAGE_EXTENSIONS)
        self.assertIn('.dng', self.extractor.IMAGE_EXTENSIONS)

    @patch('metadata_extractor.Image.open')
    @patch('metadata_extractor.cv2.imread')
    def test_extract_metadata_raw(self, mock_cv2_read, mock_pil_open):
        # Mock PIL open to simulate RAW file opening
        mock_img = MagicMock()
        mock_img.mode = 'RGB'
        mock_img._getexif.return_value = {
            36867: '2023:01:01 12:00:00', # DateTimeOriginal
            34853: { # GPSInfo
                1: 'N', 2: (10.0, 0.0, 0.0),
                3: 'E', 4: (20.0, 0.0, 0.0)
            }
        }
        mock_pil_open.return_value.__enter__.return_value = mock_img
        
        # Mock cv2 imread to fail for RAW (simulating need for fallback or PIL)
        mock_cv2_read.return_value = None

        metadata = self.extractor.extract_metadata('test.arw')
        
        self.assertEqual(metadata['file_type'], 'Image')
        self.assertEqual(metadata['date_time_original'], '2023:01:01 12:00:00')
        self.assertAlmostEqual(metadata['gps_latitude'], 10.0)
        self.assertAlmostEqual(metadata['gps_longitude'], 20.0)

    @patch('metadata_extractor.Image.open')
    def test_thumbnail_generation_raw(self, mock_pil_open):
        mock_img = MagicMock()
        mock_img.mode = 'RGB'
        mock_img.width = 1000
        mock_img.height = 800
        mock_pil_open.return_value.__enter__.return_value = mock_img
        
        # Mock os.path.exists to return False so it tries to generate
        with patch('os.path.exists', return_value=False):
            # Mock os.makedirs
            with patch('os.makedirs'):
                # Mock image save
                with patch.object(mock_img, 'save') as mock_save:
                    # We need to mock Image.new as well since it's used in _generate_thumbnail
                    with patch('PIL.Image.new') as mock_new:
                        mock_thumb = MagicMock()
                        mock_new.return_value = mock_thumb
                        
                        path = self.extractor._generate_thumbnail('test.cr2', 'Image')
                        
                        self.assertIsNotNone(path)
                        self.assertTrue(path.endswith('.jpg'))

if __name__ == '__main__':
    unittest.main()
