"""
MediaVault Scanner - GGUF OCR Module
Implements high-performance OCR using Deepseek GGUF model via llama-cpp-python with Tesseract fallback.
Supports both NVIDIA CUDA and AMD ROCm/HIP acceleration.
"""

import os
import logging
import subprocess
from typing import Tuple, Optional, Union
from pathlib import Path
import numpy as np
from PIL import Image
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GGUF_OCR:
    """
    GGUF-based OCR engine with intelligent fallback and cross-GPU support.
    
    Priority:
    1. Deepseek GGUF (high-performance, requires llama-cpp-python with GPU support)
    2. Tesseract (fallback, lightweight)
    
    Supports:
    - NVIDIA CUDA acceleration
    - AMD ROCm/HIP acceleration
    - CPU fallback
    """
    
    def __init__(self, config: dict = None):
        """
        Initialize GGUF OCR engine.
        
        Args:
            config: Configuration dictionary with model paths and settings
        """
        self.config = config or {}
        self.deepseek_available = False
        self.tesseract_available = False
        self.current_engine = None
        self.gpu_type = None  # 'cuda', 'rocm', or 'cpu'
        
        # Model components
        self.model = None
        
        # Initialize engines
        self._initialize_deepseek_gguf()
        self._initialize_tesseract()
        
        # Log initialization status
        if self.deepseek_available:
            logger.info(f"✓ Deepseek GGUF initialized successfully (Primary OCR, GPU: {self.gpu_type})")
            self.current_engine = "deepseek_gguf"
        elif self.tesseract_available:
            logger.info("✓ Tesseract initialized successfully (Fallback OCR)")
            self.current_engine = "tesseract"
        else:
            logger.warning("⚠ No OCR engine available - OCR features will be disabled")
            self.current_engine = None
    
    def _detect_gpu_type(self) -> str:
        """
        Detect available GPU type (CUDA, ROCm, or CPU).
        
        Returns:
            'cuda', 'rocm', or 'cpu'
        """
        try:
            # Check for NVIDIA CUDA
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                return 'cuda'
        except:
            pass
        
        try:
            # Check for AMD ROCm
            result = subprocess.run(['rocm-smi'], capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                return 'rocm'
        except:
            pass
        
        return 'cpu'
    
    def _initialize_deepseek_gguf(self):
        """Initialize Deepseek GGUF model via llama-cpp-python."""
        try:
            # Check if Deepseek is enabled
            if not self.config.get('deepseek_enabled', True):
                logger.info("Deepseek GGUF disabled in configuration")
                return
            
            # Try to import llama-cpp-python
            try:
                from llama_cpp import Llama
            except ImportError:
                logger.warning("llama-cpp-python not installed")
                logger.info("Install with GPU support:")
                logger.info("  NVIDIA: FORCE_CMAKE=1 CMAKE_ARGS=\"-DLLAMA_CUBLAS=on\" pip install llama-cpp-python --no-cache-dir")
                logger.info("  AMD: FORCE_CMAKE=1 CMAKE_ARGS=\"-DLLAMA_HIP=on\" pip install llama-cpp-python --no-cache-dir")
                return
            
            # Get GGUF model path
            gguf_path = self.config.get('deepseek_gguf_path', 'models/deepseek-ocr.gguf')
            
            # Check if model file exists
            if not os.path.exists(gguf_path):
                logger.warning(f"GGUF model file not found: {gguf_path}")
                logger.info(f"Please place the Deepseek GGUF model at: {gguf_path}")
                # Create models directory if it doesn't exist
                model_dir = os.path.dirname(gguf_path)
                if model_dir and not os.path.exists(model_dir):
                    os.makedirs(model_dir, exist_ok=True)
                    logger.info(f"Created directory: {model_dir}")
                return
            
            logger.info(f"Loading Deepseek GGUF model from: {gguf_path}")
            
            # Get configuration
            use_gpu = self.config.get('use_gpu', True)
            gpu_layers = self.config.get('gpu_layers', -1)  # -1 = all layers
            n_ctx = self.config.get('n_ctx', 2048)
            n_threads = self.config.get('n_threads', 4)
            
            # Detect GPU type
            self.gpu_type = self._detect_gpu_type()
            
            # Load model with appropriate settings
            if use_gpu and self.gpu_type in ['cuda', 'rocm']:
                logger.info(f"Attempting to use {self.gpu_type.upper()} acceleration...")
                self.model = Llama(
                    model_path=gguf_path,
                    n_gpu_layers=gpu_layers,
                    n_ctx=n_ctx,
                    n_threads=n_threads,
                    verbose=False
                )
            else:
                logger.info("Using CPU-only mode...")
                self.gpu_type = 'cpu'
                self.model = Llama(
                    model_path=gguf_path,
                    n_gpu_layers=0,  # CPU only
                    n_ctx=n_ctx,
                    n_threads=n_threads,
                    verbose=False
                )
            
            self.deepseek_available = True
            logger.info(f"✓ Deepseek GGUF model loaded successfully ({self.gpu_type.upper()})")

        except Exception as e:
            logger.warning(f"Failed to initialize Deepseek GGUF: {e}")
            logger.info("Falling back to Tesseract OCR")

    def _initialize_tesseract(self):
        """Initialize Tesseract OCR as fallback."""
        try:
            import pytesseract

            # Check if custom Tesseract path is specified
            tesseract_path = self.config.get('tesseract_path')
            if tesseract_path and os.path.exists(tesseract_path):
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
                logger.info(f"Using Tesseract from: {tesseract_path}")

            # Test Tesseract availability
            try:
                version = pytesseract.get_tesseract_version()
                self.tesseract_available = True
                logger.info(f"✓ Tesseract {version} available")
            except Exception as e:
                logger.warning(f"Tesseract not available: {e}")
                logger.info("Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki")

        except ImportError:
            logger.warning("pytesseract not installed")
            logger.info("Install with: pip install pytesseract")

    def extract_text(self, image_input: Union[str, np.ndarray, Image.Image], max_length: int = 100) -> Tuple[str, str]:
        """
        Extract text from image using available OCR engine.

        Args:
            image_input: Image file path, numpy array, or PIL Image
            max_length: Maximum length of OCR text summary

        Returns:
            Tuple of (ocr_text_summary, keywords)
        """
        # Try Deepseek GGUF first
        if self.deepseek_available:
            try:
                return self._extract_with_deepseek_gguf(image_input, max_length)
            except Exception as e:
                logger.warning(f"Deepseek GGUF extraction failed: {e}")
                logger.info("Falling back to Tesseract...")

        # Fall back to Tesseract
        if self.tesseract_available:
            try:
                return self._extract_with_tesseract(image_input, max_length)
            except Exception as e:
                logger.warning(f"Tesseract extraction failed: {e}")

        # No OCR available
        return "", ""

    def _extract_with_deepseek_gguf(self, image_input: Union[str, np.ndarray, Image.Image], max_length: int) -> Tuple[str, str]:
        """
        Extract text using Deepseek GGUF model.

        Args:
            image_input: Image file path, numpy array, or PIL Image
            max_length: Maximum length of OCR text summary

        Returns:
            Tuple of (ocr_text_summary, keywords)
        """
        # Convert input to PIL Image
        if isinstance(image_input, str):
            image = Image.open(image_input).convert('RGB')
        elif isinstance(image_input, np.ndarray):
            image = Image.fromarray(image_input).convert('RGB')
        elif isinstance(image_input, Image.Image):
            image = image_input.convert('RGB')
        else:
            raise ValueError(f"Unsupported image input type: {type(image_input)}")

        # Save image temporarily for GGUF model (llama-cpp-python requires file path for vision models)
        temp_path = "temp_ocr_image.jpg"
        image.save(temp_path, 'JPEG')

        try:
            # Create OCR prompt
            prompt = "Extract all visible text from this image. Provide only the text content, no descriptions."

            # Run inference
            response = self.model.create_chat_completion(
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"file://{os.path.abspath(temp_path)}"}}
                        ]
                    }
                ],
                max_tokens=512,
                temperature=0.1
            )

            # Extract text from response
            ocr_text = response['choices'][0]['message']['content'].strip()

            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)

            # Extract keywords and create summary
            keywords = self._extract_keywords(ocr_text)
            summary = ocr_text[:max_length] if len(ocr_text) > max_length else ocr_text

            return summary, keywords

        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e

    def _extract_with_tesseract(self, image_input: Union[str, np.ndarray, Image.Image], max_length: int) -> Tuple[str, str]:
        """
        Extract text using Tesseract OCR.

        Args:
            image_input: Image file path, numpy array, or PIL Image
            max_length: Maximum length of OCR text summary

        Returns:
            Tuple of (ocr_text_summary, keywords)
        """
        import pytesseract

        # Convert input to PIL Image
        if isinstance(image_input, str):
            image = Image.open(image_input)
        elif isinstance(image_input, np.ndarray):
            image = Image.fromarray(image_input)
        elif isinstance(image_input, Image.Image):
            image = image_input
        else:
            raise ValueError(f"Unsupported image input type: {type(image_input)}")

        # Extract text
        ocr_text = pytesseract.image_to_string(image).strip()

        # Extract keywords and create summary
        keywords = self._extract_keywords(ocr_text)
        summary = ocr_text[:max_length] if len(ocr_text) > max_length else ocr_text

        return summary, keywords

    def _extract_keywords(self, text: str, max_keywords: int = 10) -> str:
        """
        Extract meaningful keywords from OCR text.

        Args:
            text: Input text
            max_keywords: Maximum number of keywords to extract

        Returns:
            Comma-separated keywords
        """
        if not text:
            return ""

        # Remove special characters and split into words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())

        # Common stop words to filter out
        stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'}

        # Filter and count words
        word_freq = {}
        for word in words:
            if word not in stop_words and len(word) > 2:
                word_freq[word] = word_freq.get(word, 0) + 1

        # Sort by frequency and get top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        keywords = [word for word, freq in sorted_words[:max_keywords]]

        return ', '.join(keywords)

    def get_engine_status(self) -> dict:
        """
        Get current OCR engine status.

        Returns:
            Dictionary with engine status information
        """
        return {
            'current_engine': self.current_engine,
            'deepseek_available': self.deepseek_available,
            'tesseract_available': self.tesseract_available,
            'gpu_type': self.gpu_type if self.deepseek_available else None
        }

