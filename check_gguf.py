"""Check GGUF model file validity"""
import os

model_path = "models/deepseek-ocr.gguf"

if os.path.exists(model_path):
    with open(model_path, 'rb') as f:
        magic = f.read(4)
        print(f"File magic bytes: {magic}")
        print(f"Is GGUF format: {magic == b'GGUF'}")
        print(f"File size: {os.path.getsize(model_path) / (1024*1024):.2f} MB")
else:
    print(f"Model file not found: {model_path}")

