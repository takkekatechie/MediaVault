"""
Test script for GGUF OCR module
Tests initialization and basic functionality
"""

import os
from gguf_ocr import GGUF_OCR
from config import Config

def test_gguf_ocr_initialization():
    """Test GGUF OCR initialization."""
    print("=" * 60)
    print("Testing GGUF OCR Initialization")
    print("=" * 60)
    
    # Load configuration
    Config.load_config()
    config = Config.get_gguf_ocr_config()
    
    print(f"\nConfiguration:")
    print(f"  GGUF Path: {config['deepseek_gguf_path']}")
    print(f"  Model Folder: {config['model_folder']}")
    print(f"  Use GPU: {config['use_gpu']}")
    print(f"  GPU Layers: {config['gpu_layers']}")
    print(f"  Context Size: {config['n_ctx']}")
    print(f"  CPU Threads: {config['n_threads']}")
    print(f"  Deepseek Enabled: {config['deepseek_enabled']}")
    print(f"  Tesseract Path: {config['tesseract_path']}")
    print(f"  Tesseract Enabled: {config['tesseract_enabled']}")
    
    # Initialize GGUF OCR
    print("\n" + "-" * 60)
    print("Initializing GGUF OCR Engine...")
    print("-" * 60)
    
    ocr = GGUF_OCR(config=config)
    
    # Get engine status
    status = ocr.get_engine_status()
    
    print("\n" + "=" * 60)
    print("GGUF OCR Engine Status")
    print("=" * 60)
    print(f"  Current Engine: {status['current_engine']}")
    print(f"  Deepseek Available: {status['deepseek_available']}")
    print(f"  Tesseract Available: {status['tesseract_available']}")
    print(f"  GPU Type: {status['gpu_type']}")
    
    # Check model file existence
    print("\n" + "=" * 60)
    print("Model File Status")
    print("=" * 60)
    gguf_path = config['deepseek_gguf_path']
    if os.path.exists(gguf_path):
        file_size_mb = os.path.getsize(gguf_path) / (1024 * 1024)
        print(f"  ✅ GGUF model found: {gguf_path}")
        print(f"  📦 File size: {file_size_mb:.2f} MB")
    else:
        print(f"  ⚠️ GGUF model NOT found: {gguf_path}")
        print(f"  📝 Please place the Deepseek GGUF model at this location")
        
        # Check if models directory exists
        model_dir = os.path.dirname(gguf_path)
        if model_dir and os.path.exists(model_dir):
            print(f"  ✅ Models directory exists: {model_dir}")
        else:
            print(f"  ⚠️ Models directory does not exist: {model_dir}")
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    if status['deepseek_available']:
        print(f"  ✅ Deepseek GGUF OCR is READY ({status['gpu_type'].upper()})")
    elif status['tesseract_available']:
        print("  ⚠️ Deepseek GGUF unavailable, using Tesseract fallback")
    else:
        print("  ❌ No OCR engine available!")
        print("  📝 Please install llama-cpp-python and/or Tesseract")
    
    print("\n" + "=" * 60)
    print("Installation Instructions")
    print("=" * 60)
    
    if not status['deepseek_available']:
        print("\n🔧 To enable Deepseek GGUF OCR:")
        print("\n1. Install llama-cpp-python with GPU support:")
        print("\n   For NVIDIA CUDA (PowerShell):")
        print("   $env:FORCE_CMAKE=1")
        print("   $env:CMAKE_ARGS=\"-DLLAMA_CUBLAS=on\"")
        print("   pip install llama-cpp-python --no-cache-dir")
        print("\n   For AMD ROCm/HIP (PowerShell):")
        print("   $env:FORCE_CMAKE=1")
        print("   $env:CMAKE_ARGS=\"-DLLAMA_HIP=on\"")
        print("   pip install llama-cpp-python --no-cache-dir")
        print("\n   For CPU-only:")
        print("   pip install llama-cpp-python")
        print(f"\n2. Place GGUF model file at: {gguf_path}")
    
    if not status['tesseract_available']:
        print("\n🔧 To enable Tesseract OCR:")
        print("\n1. Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Install Tesseract")
        print("3. Add to PATH or configure path in application")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
    
    return ocr, status


if __name__ == "__main__":
    try:
        ocr, status = test_gguf_ocr_initialization()
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

