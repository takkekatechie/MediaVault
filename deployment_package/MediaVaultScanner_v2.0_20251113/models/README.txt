MediaVault Scanner - GGUF Model Folder
========================================

This folder should contain the Deepseek GGUF model file.

REQUIRED FILE:
--------------
deepseek-ocr.gguf  (2-7GB depending on quantization level)

DOWNLOAD INSTRUCTIONS:
----------------------
1. Download the Deepseek GGUF model file from your model source
2. Place it in this folder as: deepseek-ocr.gguf
3. Use the download script: ..\scripts\download_model.ps1

ALTERNATIVE:
------------
If you don't have the GGUF model, the application will automatically
fall back to Tesseract OCR (which you must install separately).

For more information, see README.md in the parent folder.
