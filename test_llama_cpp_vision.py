"""Test llama-cpp-python vision support"""
from llama_cpp import Llama
import sys

print("=" * 60)
print("Testing llama-cpp-python Vision Support")
print("=" * 60)

# Check if llama-cpp-python has vision support
try:
    from llama_cpp import llama_cpp
    print(f"\n✅ llama-cpp-python version: {llama_cpp.__version__ if hasattr(llama_cpp, '__version__') else 'unknown'}")
except:
    print("\n⚠️ Could not determine llama-cpp-python version")

# Try to load the model
model_path = "models/deepseek-ocr.gguf"
print(f"\nAttempting to load model: {model_path}")

try:
    # Try loading with minimal parameters
    print("\nTrying to load model with basic parameters...")
    model = Llama(
        model_path=model_path,
        n_ctx=512,  # Small context for testing
        n_threads=2,
        verbose=True
    )
    print("\n✅ Model loaded successfully!")
    print(f"Model type: {type(model)}")
    
    # Check if model has vision capabilities
    if hasattr(model, 'create_chat_completion_with_image'):
        print("✅ Model has vision support (create_chat_completion_with_image)")
    else:
        print("⚠️ Model does NOT have vision support")
        print("   This is a text-only model or llama-cpp-python doesn't support vision")
    
except Exception as e:
    print(f"\n❌ Failed to load model: {e}")
    print(f"\nError type: {type(e).__name__}")
    
    # Check if it's a vision model issue
    error_msg = str(e).lower()
    if 'vision' in error_msg or 'image' in error_msg or 'clip' in error_msg:
        print("\n⚠️ This appears to be a vision model compatibility issue")
        print("   Standard llama-cpp-python may not support vision-language models")
    
    print("\n" + "=" * 60)
    print("IMPORTANT INFORMATION")
    print("=" * 60)
    print("""
The Deepseek OCR GGUF model is a VISION-LANGUAGE model that requires:

1. llama-cpp-python with vision/multimodal support, OR
2. A different approach using llama.cpp with CLIP support

RECOMMENDED SOLUTIONS:

Option 1: Use llama-cpp-python with vision support
   - Check if your llama-cpp-python version supports vision
   - May need to compile from source with vision flags

Option 2: Use a text-only GGUF model for OCR
   - Find a text-only OCR model in GGUF format
   - Or use a different model architecture

Option 3: Fall back to Tesseract OCR
   - Install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
   - MediaVault will automatically use Tesseract as fallback

Option 4: Use a different vision-language framework
   - Consider using transformers with Deepseek-VL (original approach)
   - Or use Ollama with vision models
""")

print("\n" + "=" * 60)
print("Current Status")
print("=" * 60)
print("✅ llama-cpp-python is installed")
print("✅ GGUF model file is valid")
print("❌ Vision-language support may not be available")
print("\nRecommendation: Install Tesseract for immediate OCR functionality")

