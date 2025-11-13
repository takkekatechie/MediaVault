"""
Test script for VL-OCR functionality.
Tests both Deepseek-VL and Tesseract fallback mechanisms.
"""

import os
from PIL import Image, ImageDraw, ImageFont
from vl_ocr import VL_OCR
from config import Config


def create_test_image_with_text(text: str, filename: str):
    """Create a test image with text."""
    # Create a white image
    img = Image.new('RGB', (800, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a larger font
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    # Draw text
    draw.text((50, 75), text, fill='black', font=font)
    
    # Save image
    img.save(filename)
    print(f"✓ Created test image: {filename}")
    return filename


def test_vl_ocr_initialization():
    """Test VL-OCR initialization."""
    print("\n" + "=" * 70)
    print("TEST 1: VL-OCR Initialization")
    print("=" * 70)
    
    # Load config
    Config.load_config()
    vl_ocr_config = Config.get_vl_ocr_config()
    
    # Initialize VL-OCR
    print("\nInitializing VL-OCR engine...")
    vl_ocr = VL_OCR(config=vl_ocr_config)
    
    # Check status
    status = vl_ocr.get_engine_status()
    
    print("\n📊 Engine Status:")
    print(f"  Deepseek Available: {status['deepseek_available']}")
    print(f"  Tesseract Available: {status['tesseract_available']}")
    print(f"  Current Engine: {status['current_engine']}")
    print(f"  Device: {status['device']}")
    
    if status['deepseek_available']:
        print("\n✅ Deepseek-VL initialized successfully!")
    elif status['tesseract_available']:
        print("\n⚠️  Deepseek-VL not available, using Tesseract fallback")
    else:
        print("\n❌ No OCR engine available!")
        return None
    
    return vl_ocr


def test_ocr_extraction(vl_ocr):
    """Test OCR text extraction."""
    print("\n" + "=" * 70)
    print("TEST 2: OCR Text Extraction")
    print("=" * 70)
    
    # Create test images
    test_cases = [
        ("Hello World! This is a test.", "test_hello.png"),
        ("MediaVault Scanner 2.0", "test_mediavault.png"),
        ("OCR Testing 12345", "test_numbers.png"),
    ]
    
    results = []
    
    for text, filename in test_cases:
        print(f"\n📝 Test Case: '{text}'")
        
        # Create test image
        img_path = create_test_image_with_text(text, filename)
        
        # Extract text
        print("  Extracting text...")
        summary, keywords = vl_ocr.extract_text(img_path, max_length=100)
        
        print(f"  Summary: {summary}")
        print(f"  Keywords: {keywords}")
        
        # Check if extraction worked
        if summary or keywords:
            print("  ✅ Extraction successful")
            results.append(True)
        else:
            print("  ⚠️  No text extracted")
            results.append(False)
        
        # Clean up
        if os.path.exists(img_path):
            os.remove(img_path)
    
    # Summary
    success_rate = (sum(results) / len(results)) * 100
    print(f"\n📊 Success Rate: {success_rate:.1f}% ({sum(results)}/{len(results)})")
    
    return success_rate > 0


def test_fallback_mechanism():
    """Test fallback from Deepseek to Tesseract."""
    print("\n" + "=" * 70)
    print("TEST 3: Fallback Mechanism")
    print("=" * 70)
    
    # Test with Deepseek disabled
    print("\n🔄 Testing with Deepseek disabled...")
    
    config = {
        'deepseek_enabled': False,
        'tesseract_enabled': True,
        'tesseract_path': Config.TESSERACT_PATH
    }
    
    vl_ocr = VL_OCR(config=config)
    status = vl_ocr.get_engine_status()
    
    print(f"  Current Engine: {status['current_engine']}")
    
    if status['current_engine'] == 'tesseract':
        print("  ✅ Fallback to Tesseract successful")
        return True
    else:
        print("  ⚠️  Fallback did not work as expected")
        return False


def test_metadata_extractor_integration():
    """Test VL-OCR integration with MetadataExtractor."""
    print("\n" + "=" * 70)
    print("TEST 4: MetadataExtractor Integration")
    print("=" * 70)
    
    from metadata_extractor import MetadataExtractor
    
    # Create test image
    test_text = "Integration Test 2025"
    img_path = create_test_image_with_text(test_text, "test_integration.png")
    
    # Initialize extractor with VL-OCR config
    print("\n🔧 Initializing MetadataExtractor with VL-OCR...")
    Config.load_config()
    vl_ocr_config = Config.get_vl_ocr_config()
    extractor = MetadataExtractor(vl_ocr_config=vl_ocr_config)
    
    # Extract metadata
    print("  Extracting metadata...")
    metadata = extractor.extract_metadata(img_path)
    
    print(f"\n📊 Extracted Metadata:")
    print(f"  File Type: {metadata.get('file_type')}")
    print(f"  OCR Summary: {metadata.get('ocr_text_summary')}")
    print(f"  Object Keywords: {metadata.get('object_keywords')}")
    
    # Clean up
    if os.path.exists(img_path):
        os.remove(img_path)
    
    # Check if OCR worked
    if metadata.get('ocr_text_summary') or metadata.get('object_keywords'):
        print("\n✅ Integration successful - OCR data extracted")
        return True
    else:
        print("\n⚠️  Integration issue - No OCR data extracted")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("MediaVault Scanner - VL-OCR Test Suite")
    print("=" * 70)
    
    results = {}
    
    # Test 1: Initialization
    vl_ocr = test_vl_ocr_initialization()
    results['initialization'] = vl_ocr is not None
    
    if vl_ocr:
        # Test 2: OCR Extraction
        results['extraction'] = test_ocr_extraction(vl_ocr)
    else:
        results['extraction'] = False
        print("\n⚠️  Skipping extraction test (no OCR engine available)")
    
    # Test 3: Fallback
    results['fallback'] = test_fallback_mechanism()
    
    # Test 4: Integration
    results['integration'] = test_metadata_extractor_integration()
    
    # Final Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name.capitalize()}: {status}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"\n📊 Overall: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
    
    if success_rate == 100:
        print("\n🎉 All tests passed! VL-OCR is working correctly.")
    elif success_rate >= 75:
        print("\n⚠️  Most tests passed. Check warnings above.")
    else:
        print("\n❌ Multiple tests failed. Please review errors above.")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()

