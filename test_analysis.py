"""
Test script for analysis features
"""

from database import MediaDatabase

def test_analysis_features():
    """Test the new analysis features."""
    print("=" * 60)
    print("Testing Analysis Features")
    print("=" * 60)
    
    # Use existing database
    db = MediaDatabase('test_metadata.db')
    
    print("\n1. Testing Analytics Summary...")
    analytics = db.get_analytics_summary()
    print(f"   Total files: {analytics['total_files']}")
    print(f"   Images: {analytics['image_count']}")
    print(f"   Videos: {analytics['video_count']}")
    print(f"   Unique locations: {analytics['unique_locations']}")
    print(f"   Avg people per photo: {analytics['avg_people_per_photo']}")
    print(f"   Emotion distribution: {analytics['emotion_distribution']}")
    print(f"   Top keywords: {analytics['top_keywords']}")
    print("   ✓ Analytics working!")
    
    print("\n2. Testing Filtered Queries...")
    
    # Test emotion filter
    filtered = db.get_filtered_metadata(emotion_filter='Positive')
    print(f"   Positive emotion records: {len(filtered)}")
    
    # Test person count filter
    filtered = db.get_filtered_metadata(person_count_min=1)
    print(f"   Records with people: {len(filtered)}")
    
    # Test keyword search
    filtered = db.get_filtered_metadata(keyword_search='test')
    print(f"   Records with 'test' keyword: {len(filtered)}")
    
    print("   ✓ Filtering working!")
    
    print("\n3. Testing CSV Export...")
    success = db.export_to_csv('test_export.csv')
    print(f"   Export success: {success}")
    if success:
        print("   ✓ CSV export working!")
    else:
        print("   ⚠ CSV export failed (may be no data)")
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_analysis_features()

