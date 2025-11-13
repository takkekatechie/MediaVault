"""
MediaVault Scanner - Test Script
Simple test script to verify metadata extraction functionality.

Usage:
    python test_extraction.py <path_to_image_or_video>
"""

import sys
import os
from metadata_extractor import MetadataExtractor
from database import MediaDatabase


def print_metadata(metadata):
    """Pretty print metadata dictionary."""
    print("\n" + "=" * 70)
    print("EXTRACTED METADATA")
    print("=" * 70)
    
    for key, value in metadata.items():
        if value is not None and value != '' and value != 0:
            print(f"{key:20s}: {value}")
    
    print("=" * 70 + "\n")


def test_single_file(filepath):
    """Test metadata extraction on a single file."""
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return
    
    print(f"Testing metadata extraction on: {filepath}")
    
    # Create extractor
    extractor = MetadataExtractor()
    
    # Extract metadata
    print("Extracting metadata...")
    metadata = extractor.extract_metadata(filepath)
    
    # Print results
    print_metadata(metadata)
    
    # Test database insertion
    print("Testing database insertion...")
    db = MediaDatabase("test_metadata.db")
    
    success = db.insert_metadata(metadata)
    
    if success:
        print("✓ Successfully inserted into database!")
        
        # Retrieve and verify
        retrieved = db.get_metadata_by_filepath(filepath)
        if retrieved:
            print("✓ Successfully retrieved from database!")
            print(f"  Record ID: {retrieved['id']}")
        else:
            print("✗ Failed to retrieve from database")
    else:
        print("✗ Failed to insert into database")


def test_database_operations():
    """Test basic database operations."""
    print("\n" + "=" * 70)
    print("TESTING DATABASE OPERATIONS")
    print("=" * 70 + "\n")
    
    db = MediaDatabase("test_metadata.db")
    
    # Test data
    test_metadata = {
        'filepath': 'C:\\test\\sample.jpg',
        'filename': 'sample.jpg',
        'file_type': 'Image',
        'date_time_original': '2025:01:15 12:30:45',
        'gps_latitude': 37.7749,
        'gps_longitude': -122.4194,
        'person_count': 3,
        'ocr_text_summary': 'Sample text from image',
        'object_keywords': 'sample, test, image',
        'emotion_sentiment': 'Positive/Vacation'
    }
    
    # Insert
    print("Inserting test record...")
    success = db.insert_metadata(test_metadata)
    print(f"  Insert: {'✓ Success' if success else '✗ Failed'}")
    
    # Check existence
    exists = db.file_exists('C:\\test\\sample.jpg')
    print(f"  File exists check: {'✓ Success' if exists else '✗ Failed'}")
    
    # Retrieve
    retrieved = db.get_metadata_by_filepath('C:\\test\\sample.jpg')
    print(f"  Retrieve: {'✓ Success' if retrieved else '✗ Failed'}")
    
    # Count
    count = db.get_record_count()
    print(f"  Record count: {count}")
    
    print("\n✓ Database operations test complete!")


def main():
    """Main test function."""
    print("\n" + "=" * 70)
    print("MediaVault Scanner - Metadata Extraction Test")
    print("=" * 70 + "\n")
    
    if len(sys.argv) > 1:
        # Test with provided file
        filepath = sys.argv[1]
        test_single_file(filepath)
    else:
        # Run database tests
        print("No file provided. Running database operation tests...\n")
        test_database_operations()
        print("\nTo test file extraction, run:")
        print("  python test_extraction.py <path_to_image_or_video>")


if __name__ == "__main__":
    main()

