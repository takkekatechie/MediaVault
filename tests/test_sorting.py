
import unittest
import sqlite3
import os
import sys

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import MediaDatabase

class TestDatabaseSorting(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_sorting.db"
        self.db = MediaDatabase(self.db_path)
        
        # Insert sample data
        sample_data = [
            {
                'filepath': '/path/to/a.jpg', 'filename': 'a.jpg', 'file_type': 'Image',
                'date_time_original': '2023:01:01 10:00:00', 'person_count': 1, 'emotion_sentiment': 'Neutral',
                'object_keywords': 'cat'
            },
            {
                'filepath': '/path/to/b.jpg', 'filename': 'b.jpg', 'file_type': 'Image',
                'date_time_original': '2023:01:02 10:00:00', 'person_count': 5, 'emotion_sentiment': 'Positive',
                'object_keywords': 'dog'
            },
            {
                'filepath': '/path/to/c.jpg', 'filename': 'c.jpg', 'file_type': 'Image',
                'date_time_original': '2023:01:03 10:00:00', 'person_count': 0, 'emotion_sentiment': 'Negative',
                'object_keywords': 'bird'
            }
        ]
        
        for data in sample_data:
            self.db.insert_metadata(data)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_sort_by_date_desc(self):
        results = self.db.get_filtered_metadata(sort_by='date_time_original', sort_order='DESC')
        self.assertEqual(results[0]['filename'], 'c.jpg')
        self.assertEqual(results[1]['filename'], 'b.jpg')
        self.assertEqual(results[2]['filename'], 'a.jpg')

    def test_sort_by_date_asc(self):
        results = self.db.get_filtered_metadata(sort_by='date_time_original', sort_order='ASC')
        self.assertEqual(results[0]['filename'], 'a.jpg')
        self.assertEqual(results[1]['filename'], 'b.jpg')
        self.assertEqual(results[2]['filename'], 'c.jpg')

    def test_sort_by_filename_asc(self):
        results = self.db.get_filtered_metadata(sort_by='filename', sort_order='ASC')
        self.assertEqual(results[0]['filename'], 'a.jpg')
        self.assertEqual(results[1]['filename'], 'b.jpg')
        self.assertEqual(results[2]['filename'], 'c.jpg')

    def test_sort_by_person_count_desc(self):
        results = self.db.get_filtered_metadata(sort_by='person_count', sort_order='DESC')
        self.assertEqual(results[0]['filename'], 'b.jpg') # 5
        self.assertEqual(results[1]['filename'], 'a.jpg') # 1
        self.assertEqual(results[2]['filename'], 'c.jpg') # 0

    def test_sort_by_emotion_asc(self):
        results = self.db.get_filtered_metadata(sort_by='emotion_sentiment', sort_order='ASC')
        # Negative < Neutral < Positive (alphabetical)
        self.assertEqual(results[0]['emotion_sentiment'], 'Negative')
        self.assertEqual(results[1]['emotion_sentiment'], 'Neutral')
        self.assertEqual(results[2]['emotion_sentiment'], 'Positive')

if __name__ == '__main__':
    unittest.main()
