"""
Test script for object/scene detection functionality.
"""

import os
from metadata_extractor import MetadataExtractor
from PIL import Image
import numpy as np

def create_test_images():
    """Create test images with different color patterns."""
    test_images = []
    
    # Create a blue sky image
    print("Creating test image: blue_sky.jpg")
    sky_img = Image.new('RGB', (800, 600), color=(135, 206, 235))  # Sky blue
    sky_img.save('test_blue_sky.jpg')
    test_images.append('test_blue_sky.jpg')
    
    # Create a green grass image
    print("Creating test image: green_grass.jpg")
    grass_img = Image.new('RGB', (800, 600), color=(34, 139, 34))  # Forest green
    grass_img.save('test_green_grass.jpg')
    test_images.append('test_green_grass.jpg')
    
    # Create a sunset image (orange/red)
    print("Creating test image: sunset.jpg")
    sunset_img = Image.new('RGB', (800, 600), color=(255, 140, 0))  # Dark orange
    sunset_img.save('test_sunset.jpg')
    test_images.append('test_sunset.jpg')
    
    # Create a mixed scene (blue top, green bottom)
    print("Creating test image: mixed_scene.jpg")
    mixed_img = Image.new('RGB', (800, 600))
    pixels = mixed_img.load()
    for y in range(600):
        for x in range(800):
            if y < 300:
                pixels[x, y] = (135, 206, 235)  # Sky blue
            else:
                pixels[x, y] = (34, 139, 34)  # Grass green
    mixed_img.save('test_mixed_scene.jpg')
    test_images.append('test_mixed_scene.jpg')
    
    return test_images

def test_object_detection():
    """Test object detection on created test images."""
    print("=" * 60)
    print("Testing Object/Scene Detection")
    print("=" * 60)
    
    # Create test images
    test_images = create_test_images()
    
    # Initialize extractor
    extractor = MetadataExtractor()
    
    print("\n" + "=" * 60)
    print("Running Object Detection Tests")
    print("=" * 60)
    
    for image_path in test_images:
        print(f"\nTesting: {image_path}")
        
        # Extract metadata
        metadata = extractor.extract_metadata(image_path)
        
        # Display results
        print(f"  File Type: {metadata.get('file_type')}")
        print(f"  Object Keywords: {metadata.get('object_keywords')}")
        print(f"  Person Count: {metadata.get('person_count')}")
        print(f"  Emotion/Sentiment: {metadata.get('emotion_sentiment')}")
        
        # Verify object_keywords is not empty
        if metadata.get('object_keywords'):
            print(f"  ✓ Object detection working")
        else:
            print(f"  ⚠ No objects detected")
    
    # Clean up test images
    print("\n" + "=" * 60)
    print("Cleaning Up Test Images")
    print("=" * 60)
    
    for image_path in test_images:
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"✓ Removed: {image_path}")
    
    print("\n" + "=" * 60)
    print("Object Detection Test Complete!")
    print("=" * 60)
    
    # Test with existing database records
    print("\n" + "=" * 60)
    print("Testing with Existing Database Records")
    print("=" * 60)
    
    from database import MediaDatabase
    db = MediaDatabase('test_metadata.db')
    
    records = db.get_all_metadata()
    
    if records:
        print(f"\nFound {len(records)} records in database")
        
        for record in records[:3]:  # Show first 3 records
            print(f"\nFile: {os.path.basename(record.get('filepath', ''))}")
            print(f"  Object Keywords: {record.get('object_keywords', 'N/A')}")
            print(f"  OCR Summary: {record.get('ocr_text_summary', 'N/A')[:50]}...")
    else:
        print("\n⚠ No records found in database")
        print("Run a scan first to test object detection on real files")
    
    print("\n" + "=" * 60)
    print("All Tests Complete!")
    print("=" * 60)
    
    print("\nNOTE: Object detection uses a simplified local heuristic based on:")
    print("  - Color analysis (sky, grass, water, sunset, foliage)")
    print("  - Edge detection (buildings, structures)")
    print("  - Shape detection (circular objects)")
    print("  - Combined with OCR keywords")
    print("\nThis is NOT ML-based detection, but a basic pattern recognition system.")

if __name__ == "__main__":
    test_object_detection()

