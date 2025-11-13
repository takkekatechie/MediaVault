"""
MediaVault Scanner - Model Setup Dialog
Guides users through Deepseek GGUF and Tesseract OCR setup.
"""

import customtkinter as ctk
from tkinter import filedialog
import os


class ModelSetupDialog(ctk.CTkToplevel):
    """Dialog for configuring OCR models (Deepseek GGUF and Tesseract)."""

    def __init__(self, parent, config):
        super().__init__(parent)

        self.config = config
        self.setup_complete = False

        # Window configuration
        self.title("Step 1: High-Performance Model Setup (Deepseek GGUF/Tesseract Fallback)")
        self.geometry("800x700")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.winfo_screenheight() // 2) - (700 // 2)
        self.geometry(f"+{x}+{y}")
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create dialog widgets."""
        
        # Main container with padding
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="🚀 MediaVault Scanner - OCR Engine Setup",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Scrollable frame for content
        scroll_frame = ctk.CTkScrollableFrame(main_frame, height=500)
        scroll_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # ===== SECTION A: Deepseek-VL Setup =====
        self._create_deepseek_section(scroll_frame)
        
        # Separator
        separator1 = ctk.CTkFrame(scroll_frame, height=2, fg_color="gray30")
        separator1.pack(fill="x", pady=20)
        
        # ===== SECTION B: Tesseract Fallback =====
        self._create_tesseract_section(scroll_frame)
        
        # Separator
        separator2 = ctk.CTkFrame(scroll_frame, height=2, fg_color="gray30")
        separator2.pack(fill="x", pady=20)
        
        # ===== SECTION C: Tesseract Path Configuration =====
        self._create_tesseract_path_section(scroll_frame)
        
        # Bottom buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x")
        
        # Skip setup button
        skip_btn = ctk.CTkButton(
            button_frame,
            text="Skip Setup (Use Tesseract Only)",
            command=self._skip_setup,
            fg_color="gray40",
            hover_color="gray50"
        )
        skip_btn.pack(side="left", padx=5)
        
        # Continue button
        continue_btn = ctk.CTkButton(
            button_frame,
            text="Continue to Application →",
            command=self._continue_setup,
            fg_color="green",
            hover_color="darkgreen"
        )
        continue_btn.pack(side="right", padx=5)
    
    def _create_deepseek_section(self, parent):
        """Create Deepseek GGUF setup section."""

        # Section header
        header = ctk.CTkLabel(
            parent,
            text="📊 Instruction A: Deepseek GGUF High-Performance OCR",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        header.pack(fill="x", pady=(0, 10))

        # Information text
        info_text = """
Deepseek OCR uses a GGUF (quantized) model file for high-performance text extraction with
cross-GPU support (NVIDIA CUDA and AMD ROCm/HIP).

⚠️ REQUIREMENTS:
• GGUF model file: deepseek-ocr.gguf (~2-7GB depending on quantization)
• llama-cpp-python library (compiled with GPU support)
• Minimum 8GB RAM (16GB recommended)
• GPU: NVIDIA (CUDA) or AMD (ROCm) - optional but highly recommended

📦 INSTALLATION STEPS:

1. Install llama-cpp-python with GPU support:

   For NVIDIA CUDA (Windows PowerShell):
   $env:FORCE_CMAKE=1
   $env:CMAKE_ARGS="-DLLAMA_CUBLAS=on"
   pip install llama-cpp-python --no-cache-dir

   For AMD ROCm/HIP (requires ROCm stack installed):
   $env:FORCE_CMAKE=1
   $env:CMAKE_ARGS="-DLLAMA_HIP=on"
   pip install llama-cpp-python --no-cache-dir

   For CPU-only (slower):
   pip install llama-cpp-python

2. Place the GGUF model file:
   Download the Deepseek OCR GGUF model and place it at:
   ./models/deepseek-ocr.gguf

   The application will create the 'models' folder automatically.

✅ STATUS: The application will automatically detect if the GGUF model is available.
If not available, it will seamlessly fall back to Tesseract OCR.
"""
        
        info_label = ctk.CTkLabel(
            parent,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="left",
            anchor="w"
        )
        info_label.pack(fill="x", pady=(0, 10))

        # GGUF model path setting
        model_frame = ctk.CTkFrame(parent, fg_color="transparent")
        model_frame.pack(fill="x", pady=10)

        model_label = ctk.CTkLabel(
            model_frame,
            text="GGUF Model File Path:",
            font=ctk.CTkFont(size=12)
        )
        model_label.pack(anchor="w")

        model_input_frame = ctk.CTkFrame(model_frame, fg_color="transparent")
        model_input_frame.pack(fill="x", pady=5)

        self.model_path_entry = ctk.CTkEntry(
            model_input_frame,
            placeholder_text="models/deepseek-ocr.gguf"
        )
        self.model_path_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        # Set current GGUF path
        self.model_path_entry.insert(0, self.config.DEEPSEEK_GGUF_PATH)

        model_browse_btn = ctk.CTkButton(
            model_input_frame,
            text="Browse",
            width=100,
            command=self._browse_gguf_file
        )
        model_browse_btn.pack(side="right")

    def _create_tesseract_section(self, parent):
        """Create Tesseract fallback section."""

        # Section header
        header = ctk.CTkLabel(
            parent,
            text="🔄 Instruction B: Tesseract OCR Fallback",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        header.pack(fill="x", pady=(0, 10))

        # Information text
        info_text = """
If the Deepseek GGUF model is not found (missing model file, llama-cpp-python not installed,
or insufficient hardware), MediaVault Scanner will automatically fall back to using Tesseract OCR.

Tesseract is a lightweight, traditional OCR engine that:
✅ Works on any hardware (no GPU required)
✅ Has minimal memory requirements
✅ Provides good accuracy for most text extraction tasks
⚠️ May have lower accuracy than Deepseek GGUF for complex or stylized text

📦 TESSERACT INSTALLATION:

1. Download Tesseract for Windows:
   Visit: https://github.com/UB-Mannheim/tesseract/wiki
   Download: tesseract-ocr-w64-setup-*.exe (latest version)

2. Run the installer:
   • Follow the installation wizard
   • Note the installation path (default: C:\\Program Files\\Tesseract-OCR)
   • Complete the installation

3. Add Tesseract to Windows PATH (RECOMMENDED):
   • Open Windows Settings → System → About
   • Click "Advanced system settings"
   • Click "Environment Variables"
   • Under "System variables", find and select "Path"
   • Click "Edit" → "New"
   • Add: C:\\Program Files\\Tesseract-OCR
   • Click "OK" to save

✅ The application will automatically detect Tesseract if it's in your PATH.
If not found, you can manually specify the path in Section C below.
"""

        info_label = ctk.CTkLabel(
            parent,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="left",
            anchor="w"
        )
        info_label.pack(fill="x", pady=(0, 10))

    def _create_tesseract_path_section(self, parent):
        """Create Tesseract path configuration section."""

        # Section header
        header = ctk.CTkLabel(
            parent,
            text="⚙️ Instruction C: Tesseract Path Configuration",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        header.pack(fill="x", pady=(0, 10))

        # Information text
        info_text = """
If the application cannot automatically detect Tesseract, you can manually specify its location here.
This is typically needed if Tesseract is not in your Windows PATH.
"""

        info_label = ctk.CTkLabel(
            parent,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="left",
            anchor="w"
        )
        info_label.pack(fill="x", pady=(0, 10))

        # Tesseract path input
        path_frame = ctk.CTkFrame(parent, fg_color="transparent")
        path_frame.pack(fill="x", pady=10)

        path_label = ctk.CTkLabel(
            path_frame,
            text="Tesseract Executable Path:",
            font=ctk.CTkFont(size=12)
        )
        path_label.pack(anchor="w")

        path_input_frame = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_input_frame.pack(fill="x", pady=5)

        self.tesseract_entry = ctk.CTkEntry(
            path_input_frame,
            placeholder_text="e.g., C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        )
        self.tesseract_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        if self.config.TESSERACT_PATH:
            self.tesseract_entry.insert(0, self.config.TESSERACT_PATH)

        tesseract_browse_btn = ctk.CTkButton(
            path_input_frame,
            text="Browse",
            width=100,
            command=self._browse_tesseract
        )
        tesseract_browse_btn.pack(side="right")

        # Auto-detect button
        auto_detect_btn = ctk.CTkButton(
            path_frame,
            text="🔍 Auto-Detect Tesseract",
            command=self._auto_detect_tesseract,
            fg_color="blue",
            hover_color="darkblue"
        )
        auto_detect_btn.pack(pady=5)

        # Status label
        self.status_label = ctk.CTkLabel(
            path_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.status_label.pack(pady=5)

    def _browse_gguf_file(self):
        """Browse for GGUF model file."""
        filepath = filedialog.askopenfilename(
            title="Select Deepseek GGUF Model File",
            filetypes=[("GGUF Files", "*.gguf"), ("All Files", "*.*")]
        )
        if filepath:
            self.model_path_entry.delete(0, "end")
            self.model_path_entry.insert(0, filepath)

    def _browse_tesseract(self):
        """Browse for Tesseract executable."""
        filepath = filedialog.askopenfilename(
            title="Select Tesseract Executable",
            filetypes=[("Executable Files", "*.exe"), ("All Files", "*.*")]
        )
        if filepath:
            self.tesseract_entry.delete(0, "end")
            self.tesseract_entry.insert(0, filepath)

    def _auto_detect_tesseract(self):
        """Auto-detect Tesseract installation."""
        if self.config.auto_detect_tesseract():
            self.tesseract_entry.delete(0, "end")
            self.tesseract_entry.insert(0, self.config.TESSERACT_PATH)
            self.status_label.configure(
                text="✅ Tesseract detected successfully!",
                text_color="green"
            )
        else:
            self.status_label.configure(
                text="⚠️ Tesseract not found. Please install or specify path manually.",
                text_color="orange"
            )

    def _skip_setup(self):
        """Skip setup and use Tesseract only."""
        # Disable Deepseek
        self.config.DEEPSEEK_ENABLED = False

        # Save configuration
        self._save_settings()

        self.setup_complete = True
        self.destroy()

    def _continue_setup(self):
        """Continue with current settings."""
        # Save configuration
        self._save_settings()

        self.setup_complete = True
        self.destroy()

    def _save_settings(self):
        """Save current settings to config."""
        # Save GGUF model path
        gguf_path = self.model_path_entry.get().strip()
        if gguf_path:
            self.config.DEEPSEEK_GGUF_PATH = gguf_path

        # Save Tesseract path
        tesseract_path = self.tesseract_entry.get().strip()
        if tesseract_path and os.path.exists(tesseract_path):
            self.config.set_tesseract_path(tesseract_path)

        # Save config to file
        self.config.save_config()

