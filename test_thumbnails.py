"""
Test script for thumbnail generation and display features.
"""

import os
from metadata_extractor import MetadataExtractor
from database import MediaDatabase

def test_thumbnail_generation():
    """Test thumbnail generation for existing test data."""
    print("=" * 60)
    print("Testing Thumbnail Generation")
    print("=" * 60)
    
    # Initialize extractor
    extractor = MetadataExtractor()
    
    # Check if thumbnails directory was created
    if os.path.exists(extractor.THUMBNAIL_DIR):
        print(f"✓ Thumbnails directory created: {extractor.THUMBNAIL_DIR}")
    else:
        print(f"✗ Thumbnails directory not found")
        return
    
    # Test with existing database
    db = MediaDatabase('test_metadata.db')
    
    # Get all records
    records = db.get_all_metadata()
    
    if not records:
        print("\n⚠ No records found in test database")
        print("Please run a scan first to test thumbnail generation")
        return
    
    print(f"\nFound {len(records)} records in database")
    
    # Check thumbnails
    thumbnails_found = 0
    for record in records:
        filepath = record.get('filepath')
        thumbnail_path = record.get('thumbnail_path')
        
        if thumbnail_path:
            if os.path.exists(thumbnail_path):
                thumbnails_found += 1
                print(f"✓ Thumbnail exists: {os.path.basename(thumbnail_path)}")
            else:
                print(f"✗ Thumbnail missing: {thumbnail_path}")
        else:
            print(f"⚠ No thumbnail path for: {os.path.basename(filepath)}")
    
    print(f"\n{thumbnails_found}/{len(records)} thumbnails found")
    
    # Test thumbnail generation for a new file
    print("\n" + "=" * 60)
    print("Testing New Thumbnail Generation")
    print("=" * 60)
    
    # Create a test image
    from PIL import Image
    test_image_path = "test_thumbnail_image.jpg"
    
    # Create a simple test image
    img = Image.new('RGB', (800, 600), color='blue')
    img.save(test_image_path)
    print(f"✓ Created test image: {test_image_path}")
    
    # Extract metadata (which should generate thumbnail)
    metadata = extractor.extract_metadata(test_image_path)
    
    if metadata.get('thumbnail_path'):
        print(f"✓ Thumbnail generated: {metadata['thumbnail_path']}")
        
        if os.path.exists(metadata['thumbnail_path']):
            print(f"✓ Thumbnail file exists")
            
            # Check thumbnail size
            thumb_img = Image.open(metadata['thumbnail_path'])
            print(f"✓ Thumbnail size: {thumb_img.size}")
            
            if thumb_img.size == (64, 64):
                print(f"✓ Thumbnail size is correct (64x64)")
            else:
                print(f"⚠ Thumbnail size is {thumb_img.size}, expected (64, 64)")
        else:
            print(f"✗ Thumbnail file not found")
    else:
        print(f"✗ No thumbnail path in metadata")
    
    # Clean up test image
    if os.path.exists(test_image_path):
        os.remove(test_image_path)
        print(f"✓ Cleaned up test image")
    
    print("\n" + "=" * 60)
    print("Thumbnail Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_thumbnail_generation()

