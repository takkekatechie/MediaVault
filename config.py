"""
MediaVault Scanner - Configuration Module
Application settings and configuration management.
"""

import os
import json
from pathlib import Path


class Config:
    """Application configuration manager."""
    
    # Application metadata
    APP_NAME = "MediaVault Scanner"
    APP_VERSION = "2.0.0"  # GGUF/llama-cpp-python Version

    # Database settings
    DEFAULT_DB_PATH = "metadata.db"

    # UI settings
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 700
    MIN_WINDOW_WIDTH = 900
    MIN_WINDOW_HEIGHT = 600

    # Theme settings
    APPEARANCE_MODE = "dark"  # "dark", "light", or "system"
    COLOR_THEME = "blue"      # "blue", "green", or "dark-blue"

    # VL-OCR Settings (Deepseek GGUF Model via llama-cpp-python)
    DEEPSEEK_GGUF_PATH = "models/deepseek-ocr.gguf"  # Path to GGUF model file
    MODEL_FOLDER = "models"  # Folder containing GGUF models

    # GPU Acceleration Settings
    USE_GPU = True  # Attempt to use GPU acceleration (CUDA or ROCm/HIP)
    GPU_LAYERS = -1  # Number of layers to offload to GPU (-1 = all layers)
    N_CTX = 2048  # Context window size
    N_THREADS = 4  # Number of CPU threads (if GPU not available)

    DEEPSEEK_ENABLED = True  # Try to use Deepseek GGUF (will fallback to Tesseract if unavailable)

    # Tesseract settings (Fallback OCR)
    TESSERACT_PATH = None  # Will be set by user or auto-detected
    TESSERACT_ENABLED = True  # Always keep Tesseract as fallback
    
    # Config file path
    CONFIG_FILE = "mediavault_config.json"
    
    @classmethod
    def load_config(cls):
        """Load configuration from file."""
        if os.path.exists(cls.CONFIG_FILE):
            try:
                with open(cls.CONFIG_FILE, 'r') as f:
                    config_data = json.load(f)

                    # VL-OCR settings (GGUF)
                    cls.DEEPSEEK_GGUF_PATH = config_data.get('deepseek_gguf_path', cls.DEEPSEEK_GGUF_PATH)
                    cls.MODEL_FOLDER = config_data.get('model_folder', cls.MODEL_FOLDER)
                    cls.USE_GPU = config_data.get('use_gpu', cls.USE_GPU)
                    cls.GPU_LAYERS = config_data.get('gpu_layers', cls.GPU_LAYERS)
                    cls.N_CTX = config_data.get('n_ctx', cls.N_CTX)
                    cls.N_THREADS = config_data.get('n_threads', cls.N_THREADS)
                    cls.DEEPSEEK_ENABLED = config_data.get('deepseek_enabled', cls.DEEPSEEK_ENABLED)

                    # Tesseract settings
                    cls.TESSERACT_PATH = config_data.get('tesseract_path')
                    cls.TESSERACT_ENABLED = config_data.get('tesseract_enabled', cls.TESSERACT_ENABLED)

                    # UI settings
                    cls.APPEARANCE_MODE = config_data.get('appearance_mode', cls.APPEARANCE_MODE)
                    cls.COLOR_THEME = config_data.get('color_theme', cls.COLOR_THEME)
            except Exception as e:
                print(f"Error loading config: {e}")

    @classmethod
    def save_config(cls):
        """Save configuration to file."""
        try:
            config_data = {
                # VL-OCR settings (GGUF)
                'deepseek_gguf_path': cls.DEEPSEEK_GGUF_PATH,
                'model_folder': cls.MODEL_FOLDER,
                'use_gpu': cls.USE_GPU,
                'gpu_layers': cls.GPU_LAYERS,
                'n_ctx': cls.N_CTX,
                'n_threads': cls.N_THREADS,
                'deepseek_enabled': cls.DEEPSEEK_ENABLED,

                # Tesseract settings
                'tesseract_path': cls.TESSERACT_PATH,
                'tesseract_enabled': cls.TESSERACT_ENABLED,

                # UI settings
                'appearance_mode': cls.APPEARANCE_MODE,
                'color_theme': cls.COLOR_THEME
            }
            with open(cls.CONFIG_FILE, 'w') as f:
                json.dump(config_data, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    @classmethod
    def set_tesseract_path(cls, path: str):
        """Set and save Tesseract path."""
        cls.TESSERACT_PATH = path
        cls.save_config()
        
        # Set pytesseract path
        try:
            import pytesseract
            pytesseract.pytesseract.tesseract_cmd = path
        except Exception as e:
            print(f"Error setting Tesseract path: {e}")
    
    @classmethod
    def auto_detect_tesseract(cls) -> bool:
        """
        Attempt to auto-detect Tesseract installation.

        Returns:
            True if Tesseract was found, False otherwise
        """
        # Common Tesseract installation paths on Windows
        common_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Tesseract-OCR\tesseract.exe",
        ]

        # Check if tesseract is in PATH
        import shutil
        tesseract_in_path = shutil.which("tesseract")
        if tesseract_in_path:
            cls.set_tesseract_path(tesseract_in_path)
            return True

        # Check common installation paths
        for path in common_paths:
            if os.path.exists(path):
                cls.set_tesseract_path(path)
                return True

        return False

    @classmethod
    def get_gguf_ocr_config(cls) -> dict:
        """
        Get GGUF OCR configuration dictionary.

        Returns:
            Dictionary with GGUF OCR settings
        """
        return {
            'deepseek_gguf_path': cls.DEEPSEEK_GGUF_PATH,
            'model_folder': cls.MODEL_FOLDER,
            'use_gpu': cls.USE_GPU,
            'gpu_layers': cls.GPU_LAYERS,
            'n_ctx': cls.N_CTX,
            'n_threads': cls.N_THREADS,
            'deepseek_enabled': cls.DEEPSEEK_ENABLED,
            'tesseract_path': cls.TESSERACT_PATH,
            'tesseract_enabled': cls.TESSERACT_ENABLED
        }

