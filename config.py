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
    APP_VERSION = "1.0.0"
    
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
    
    # Tesseract settings
    TESSERACT_PATH = None  # Will be set by user or auto-detected
    
    # Config file path
    CONFIG_FILE = "mediavault_config.json"
    
    @classmethod
    def load_config(cls):
        """Load configuration from file."""
        if os.path.exists(cls.CONFIG_FILE):
            try:
                with open(cls.CONFIG_FILE, 'r') as f:
                    config_data = json.load(f)
                    cls.TESSERACT_PATH = config_data.get('tesseract_path')
                    cls.APPEARANCE_MODE = config_data.get('appearance_mode', cls.APPEARANCE_MODE)
                    cls.COLOR_THEME = config_data.get('color_theme', cls.COLOR_THEME)
            except Exception as e:
                print(f"Error loading config: {e}")
    
    @classmethod
    def save_config(cls):
        """Save configuration to file."""
        try:
            config_data = {
                'tesseract_path': cls.TESSERACT_PATH,
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

