"""
MediaVault Scanner - Main Application (Enhanced VL-OCR Version)
A professional-grade desktop application for scanning and cataloging media metadata.
"""

import os
import sys
import threading
from pathlib import Path
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image

from config import Config
from scanner import MediaScanner
from database import MediaDatabase
from model_setup_dialog import ModelSetupDialog


class MediaVaultApp(ctk.CTk):
    """Main application window for MediaVault Scanner."""
    
    def __init__(self):
        super().__init__()
        
        # Load configuration
        Config.load_config()
        
        # Configure window
        self.title(f"{Config.APP_NAME} v{Config.APP_VERSION}")
        self.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.minsize(Config.MIN_WINDOW_WIDTH, Config.MIN_WINDOW_HEIGHT)
        
        # Set appearance
        ctk.set_appearance_mode(Config.APPEARANCE_MODE)
        ctk.set_default_color_theme(Config.COLOR_THEME)

        # Initialize scanner with GGUF OCR configuration
        gguf_ocr_config = Config.get_gguf_ocr_config()
        self.scanner = MediaScanner(gguf_ocr_config=gguf_ocr_config)
        self.scanning = False
        self.selected_directory = None

        # Screen management
        self.current_screen = "scan"  # "scan" or "analysis"
        self.scan_frame = None
        self.analysis_frame = None

        # Filtered data cache
        self.current_filtered_data = []

        # Show model setup dialog on first run or if needed
        self._show_model_setup()

        # Build UI
        self._build_ui()

        # Load existing data
        self._load_data()

    def _show_model_setup(self):
        """Show model setup dialog for VL-OCR configuration."""
        # Check if this is first run or if setup is needed
        first_run = not os.path.exists(Config.CONFIG_FILE)

        # Always show on first run, or if Tesseract is not configured
        if first_run or not Config.TESSERACT_PATH:
            # Show setup dialog after window is ready
            self.after(500, self._display_model_setup_dialog)

    def _display_model_setup_dialog(self):
        """Display the model setup dialog."""
        dialog = ModelSetupDialog(self, Config)
        self.wait_window(dialog)

        # If setup was completed, save config
        if dialog.setup_complete:
            Config.save_config()
    
    def _build_ui(self):
        """Build the main user interface."""
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create container for screens
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Build scan screen
        self._build_scan_screen()

        # Build analysis screen (hidden initially)
        self._build_analysis_screen()

        # Show scan screen by default
        self._show_screen("scan")
    
    def _show_screen(self, screen_name: str):
        """Switch between scan and analysis screens."""
        self.current_screen = screen_name

        if screen_name == "scan":
            self.scan_frame.grid(row=0, column=0, sticky="nsew")
            self.analysis_frame.grid_forget()
        else:  # analysis
            self.scan_frame.grid_forget()
            self.analysis_frame.grid(row=0, column=0, sticky="nsew")
            # Refresh analysis data
            self._refresh_analysis_dashboard()

    def _build_scan_screen(self):
        """Build the scan screen."""
        self.scan_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.scan_frame.grid_columnconfigure(0, weight=1)
        self.scan_frame.grid_rowconfigure(1, weight=1)

        # Controls Panel (Top)
        self._build_controls_panel()

        # Data View Panel (Center)
        self._build_data_view_panel()

        # Status/Log Panel (Bottom)
        self._build_status_panel()

    def _build_controls_panel(self):
        """Build the top controls panel."""
        controls_frame = ctk.CTkFrame(self.scan_frame, corner_radius=10)
        controls_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        controls_frame.grid_columnconfigure(1, weight=1)
        
        # Directory selection
        dir_label = ctk.CTkLabel(
            controls_frame,
            text="Target Directory:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        dir_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        self.dir_entry = ctk.CTkEntry(
            controls_frame,
            placeholder_text="No directory selected",
            height=40,
            font=ctk.CTkFont(size=12)
        )
        self.dir_entry.grid(row=0, column=1, padx=(10, 10), pady=15, sticky="ew")
        
        self.browse_btn = ctk.CTkButton(
            controls_frame,
            text="Browse",
            command=self._browse_directory,
            width=120,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.browse_btn.grid(row=0, column=2, padx=(0, 10), pady=15)
        
        self.scan_btn = ctk.CTkButton(
            controls_frame,
            text="Start Scan",
            command=self._start_scan,
            width=140,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2B7A0B",
            hover_color="#1F5A08",
            state="disabled"
        )
        self.scan_btn.grid(row=0, column=3, padx=(0, 20), pady=15)
        
        # Options
        self.update_existing_var = ctk.BooleanVar(value=False)
        self.update_checkbox = ctk.CTkCheckBox(
            controls_frame,
            text="Update existing records",
            variable=self.update_existing_var,
            font=ctk.CTkFont(size=12)
        )
        self.update_checkbox.grid(row=1, column=1, padx=10, pady=(0, 15), sticky="w")
    
    def _build_data_view_panel(self):
        """Build the center data view panel."""
        data_frame = ctk.CTkFrame(self.scan_frame, corner_radius=10)
        data_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        data_frame.grid_columnconfigure(0, weight=1)
        data_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        header_label = ctk.CTkLabel(
            data_frame,
            text="Scanned Media Files",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        header_label.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="w")
        
        # Create scrollable frame for data
        self.data_scroll = ctk.CTkScrollableFrame(data_frame, corner_radius=5)
        self.data_scroll.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
        self.data_scroll.grid_columnconfigure(0, weight=1)
        
        # Table header
        self._create_table_header()

    def _create_table_header(self):
        """Create the table header row."""
        header_frame = ctk.CTkFrame(self.data_scroll, fg_color="#1F538D", corner_radius=5)
        header_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        header_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        headers = ["Filename", "Date/Time Original", "Person Count", "Summary"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="white"
            )
            label.grid(row=0, column=i, padx=10, pady=10, sticky="w")

    def _build_status_panel(self):
        """Build the bottom status/log panel."""
        status_frame = ctk.CTkFrame(self.scan_frame, corner_radius=10)
        status_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")
        status_frame.grid_columnconfigure(0, weight=1)

        # Status label
        status_label = ctk.CTkLabel(
            status_frame,
            text="Status & Progress",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        status_label.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(status_frame, height=20)
        self.progress_bar.grid(row=1, column=0, padx=20, pady=(5, 10), sticky="ew")
        self.progress_bar.set(0)

        # Status text
        self.status_text = ctk.CTkTextbox(
            status_frame,
            height=100,
            font=ctk.CTkFont(size=11),
            wrap="word"
        )
        self.status_text.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="ew")
        self.status_text.insert("1.0", "Ready to scan. Please select a target directory.\n")
        self.status_text.configure(state="disabled")

    def _browse_directory(self):
        """Open directory browser dialog."""
        directory = filedialog.askdirectory(title="Select Directory to Scan")
        if directory:
            self.selected_directory = directory
            self.dir_entry.delete(0, "end")
            self.dir_entry.insert(0, directory)
            self.scan_btn.configure(state="normal")
            self._log_status(f"Selected directory: {directory}")

    def _start_scan(self):
        """Start the scanning process."""
        if not self.selected_directory:
            self._log_status("ERROR: No directory selected!")
            return

        if self.scanning:
            # Stop scan
            self.scanner.stop_scan()
            self.scanning = False
            self.scan_btn.configure(text="Start Scan", fg_color="#2B7A0B", hover_color="#1F5A08")
            self._log_status("Scan stopped by user.")
            # Transition to analysis screen after stop
            self.after(500, lambda: self._show_screen("analysis"))
            return

        # Start scan in separate thread
        self.scanning = True
        self.scan_btn.configure(text="Stop Scan", fg_color="#8B0000", hover_color="#660000")
        self.browse_btn.configure(state="disabled")

        scan_thread = threading.Thread(target=self._run_scan, daemon=True)
        scan_thread.start()

    def _run_scan(self):
        """Run the scan in a background thread."""
        self._log_status(f"Starting scan of: {self.selected_directory}")
        self._log_status("=" * 60)

        update_existing = self.update_existing_var.get()

        try:
            stats = self.scanner.scan_directory(
                self.selected_directory,
                progress_callback=self._update_progress,
                update_existing=update_existing
            )

            # Log results
            self._log_status("=" * 60)
            self._log_status("Scan completed!")
            self._log_status(f"Total files found: {stats['total_found']}")
            self._log_status(f"Processed: {stats['processed']}")
            self._log_status(f"New records: {stats['new_records']}")
            self._log_status(f"Updated records: {stats['updated_records']}")
            self._log_status(f"Skipped: {stats['skipped']}")
            self._log_status(f"Errors: {stats['errors']}")

            # Reload data
            self.after(0, self._load_data)

            # Transition to analysis screen
            self.after(500, lambda: self._show_screen("analysis"))

        except Exception as e:
            self._log_status(f"ERROR: {str(e)}")

        finally:
            self.scanning = False
            self.after(0, lambda: self.scan_btn.configure(
                text="Start Scan",
                fg_color="#2B7A0B",
                hover_color="#1F5A08"
            ))
            self.after(0, lambda: self.browse_btn.configure(state="normal"))
            self.after(0, lambda: self.progress_bar.set(0))

    def _update_progress(self, current: int, total: int, filename: str):
        """Update progress bar and status."""
        progress = current / total if total > 0 else 0
        self.after(0, lambda: self.progress_bar.set(progress))
        self.after(0, lambda: self._log_status(f"Processing file {current} of {total}: {filename}"))

    def _log_status(self, message: str):
        """Add a message to the status log."""
        self.status_text.configure(state="normal")
        self.status_text.insert("end", f"{message}\n")
        self.status_text.see("end")
        self.status_text.configure(state="disabled")

    def _load_data(self):
        """Load and display data from the database."""
        # Clear existing data rows (keep header)
        for widget in self.data_scroll.winfo_children()[1:]:
            widget.destroy()

        # Get data from database
        records = self.scanner.get_database().get_all_metadata()

        # Display records
        for i, record in enumerate(records[:100], start=1):  # Limit to 100 for performance
            self._create_data_row(i, record)

        # Update status
        total_records = self.scanner.get_database().get_record_count()
        self._log_status(f"Loaded {min(len(records), 100)} of {total_records} records from database.")

    def _create_data_row(self, row_num: int, record: dict):
        """Create a data row in the table."""
        row_frame = ctk.CTkFrame(
            self.data_scroll,
            fg_color="#2B2B2B" if row_num % 2 == 0 else "#1E1E1E",
            corner_radius=3
        )
        row_frame.grid(row=row_num, column=0, padx=5, pady=2, sticky="ew")
        row_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Filename
        filename_label = ctk.CTkLabel(
            row_frame,
            text=record.get('filename', 'N/A')[:30],
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        filename_label.grid(row=0, column=0, padx=10, pady=8, sticky="w")

        # Date/Time
        datetime_label = ctk.CTkLabel(
            row_frame,
            text=record.get('date_time_original', 'N/A')[:19],
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        datetime_label.grid(row=0, column=1, padx=10, pady=8, sticky="w")

        # Person Count
        person_label = ctk.CTkLabel(
            row_frame,
            text=str(record.get('person_count', 0)),
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        person_label.grid(row=0, column=2, padx=10, pady=8, sticky="w")

        # Summary
        summary = record.get('ocr_text_summary', '') or record.get('emotion_sentiment', 'N/A')
        summary_label = ctk.CTkLabel(
            row_frame,
            text=summary[:40],
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        summary_label.grid(row=0, column=3, padx=10, pady=8, sticky="w")

    def _build_analysis_screen(self):
        """Build the analysis and export screen."""
        self.analysis_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.analysis_frame.grid_columnconfigure(0, weight=1)
        self.analysis_frame.grid_rowconfigure(1, weight=1)

        # Top bar with back button
        top_bar = ctk.CTkFrame(self.analysis_frame, corner_radius=10)
        top_bar.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        top_bar.grid_columnconfigure(1, weight=1)

        back_btn = ctk.CTkButton(
            top_bar,
            text="← Back to Scan",
            command=lambda: self._show_screen("scan"),
            width=150,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        back_btn.grid(row=0, column=0, padx=20, pady=15)

        title_label = ctk.CTkLabel(
            top_bar,
            text="Analysis & Export Dashboard",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.grid(row=0, column=1, padx=20, pady=15)

        export_btn = ctk.CTkButton(
            top_bar,
            text="📊 Export Data",
            command=self._export_data,
            width=150,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2B7A0B",
            hover_color="#1F5A08"
        )
        export_btn.grid(row=0, column=2, padx=20, pady=15)

        # Main content area
        content_frame = ctk.CTkFrame(self.analysis_frame, corner_radius=10)
        content_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)

        # Left panel - Key Insights
        self._build_insights_panel(content_frame)

        # Right panel - Filtered Data View
        self._build_filtered_data_panel(content_frame)

    def _build_insights_panel(self, parent):
        """Build the key insights panel."""
        insights_frame = ctk.CTkFrame(parent, corner_radius=10)
        insights_frame.grid(row=0, column=0, rowspan=2, padx=(15, 10), pady=15, sticky="nsew")
        insights_frame.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkLabel(
            insights_frame,
            text="📊 Key Insights",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        header.grid(row=0, column=0, padx=20, pady=(20, 15), sticky="w")

        # Insights container
        self.insights_container = ctk.CTkScrollableFrame(insights_frame, corner_radius=5)
        self.insights_container.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
        insights_frame.grid_rowconfigure(1, weight=1)

    def _build_filtered_data_panel(self, parent):
        """Build the filtered data view panel."""
        data_panel = ctk.CTkFrame(parent, corner_radius=10)
        data_panel.grid(row=0, column=1, rowspan=2, padx=(10, 15), pady=15, sticky="nsew")
        data_panel.grid_columnconfigure(0, weight=1)
        data_panel.grid_rowconfigure(2, weight=1)

        # Header
        header = ctk.CTkLabel(
            data_panel,
            text="🔍 Filter & View Data",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        header.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Filters
        self._build_filter_controls(data_panel)

        # Data table
        self.filtered_data_scroll = ctk.CTkScrollableFrame(data_panel, corner_radius=5)
        self.filtered_data_scroll.grid(row=2, column=0, padx=15, pady=(10, 15), sticky="nsew")
        self.filtered_data_scroll.grid_columnconfigure(0, weight=1)

        # Create table header
        self._create_filtered_table_header()

    def _build_filter_controls(self, parent):
        """Build the filter controls."""
        filter_frame = ctk.CTkFrame(parent, fg_color="transparent")
        filter_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        filter_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Emotion filter
        emotion_label = ctk.CTkLabel(
            filter_frame,
            text="Emotion:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        emotion_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.emotion_filter = ctk.CTkComboBox(
            filter_frame,
            values=["All", "Positive", "Neutral", "Negative"],
            command=self._apply_filters,
            width=150
        )
        self.emotion_filter.set("All")
        self.emotion_filter.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # Person count filter
        person_label = ctk.CTkLabel(
            filter_frame,
            text="Person Count:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        person_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        person_range_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        person_range_frame.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        person_range_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.person_min = ctk.CTkEntry(person_range_frame, placeholder_text="Min", width=60)
        self.person_min.grid(row=0, column=0, padx=2)

        ctk.CTkLabel(person_range_frame, text="-").grid(row=0, column=1, padx=2)

        self.person_max = ctk.CTkEntry(person_range_frame, placeholder_text="Max", width=60)
        self.person_max.grid(row=0, column=2, padx=2)

        # Keyword search
        keyword_label = ctk.CTkLabel(
            filter_frame,
            text="Keywords:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        keyword_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.keyword_search = ctk.CTkEntry(
            filter_frame,
            placeholder_text="Search keywords...",
            width=150
        )
        self.keyword_search.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        # Apply button
        apply_btn = ctk.CTkButton(
            filter_frame,
            text="Apply Filters",
            command=self._apply_filters,
            width=120,
            height=32,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        apply_btn.grid(row=2, column=0, columnspan=3, pady=10)

    def _create_filtered_table_header(self):
        """Create the filtered data table header."""
        header_frame = ctk.CTkFrame(self.filtered_data_scroll, fg_color="#1F538D", corner_radius=5)
        header_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        header_frame.grid_columnconfigure((1, 2, 3, 4, 5), weight=1)
        header_frame.grid_columnconfigure(0, weight=0, minsize=80)  # Fixed width for thumbnail column

        headers = ["Preview", "Filename", "Date/Time", "People", "Emotion", "Keywords"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="white"
            )
            label.grid(row=0, column=i, padx=8, pady=8, sticky="w")

    def _refresh_analysis_dashboard(self):
        """Refresh the analysis dashboard with current data."""
        # Get analytics summary
        db = self.scanner.get_database()
        analytics = db.get_analytics_summary()

        # Clear insights container
        for widget in self.insights_container.winfo_children():
            widget.destroy()

        # Display insights
        self._create_insight_card("Total Files Scanned",
                                 f"{analytics['total_files']} files",
                                 f"Images: {analytics['image_count']} | Videos: {analytics['video_count']}")

        self._create_insight_card("Geographic Distribution",
                                 f"{analytics['unique_locations']} unique locations",
                                 "Files with GPS coordinates")

        self._create_insight_card("Average People Per Photo",
                                 f"{analytics['avg_people_per_photo']:.1f} people",
                                 "Based on face detection")

        # Emotion distribution
        emotion_dist = analytics['emotion_distribution']
        if emotion_dist:
            total_with_emotion = sum(emotion_dist.values())
            dominant_emotion = max(emotion_dist.items(), key=lambda x: x[1])
            percentage = (dominant_emotion[1] / total_with_emotion * 100) if total_with_emotion > 0 else 0

            self._create_insight_card("Dominant Emotion/Sentiment",
                                     f"{dominant_emotion[0]}",
                                     f"{percentage:.1f}% of classified files")
        else:
            self._create_insight_card("Dominant Emotion/Sentiment",
                                     "No data",
                                     "No emotion data available")

        # Top keywords
        top_keywords = analytics['top_keywords']
        if top_keywords:
            keywords_str = ", ".join(top_keywords)
            self._create_insight_card("Top 3 OCR Keywords",
                                     keywords_str,
                                     "Most frequently detected")
        else:
            self._create_insight_card("Top 3 OCR Keywords",
                                     "No keywords",
                                     "No OCR data available")

        # Load all data initially
        self._apply_filters()

    def _create_insight_card(self, title: str, value: str, subtitle: str):
        """Create an insight card."""
        card = ctk.CTkFrame(self.insights_container, corner_radius=8, fg_color="#2B2B2B")
        card.pack(fill="x", padx=10, pady=8)

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#888888"
        )
        title_label.pack(anchor="w", padx=15, pady=(12, 5))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFFFFF"
        )
        value_label.pack(anchor="w", padx=15, pady=5)

        subtitle_label = ctk.CTkLabel(
            card,
            text=subtitle,
            font=ctk.CTkFont(size=10),
            text_color="#AAAAAA"
        )
        subtitle_label.pack(anchor="w", padx=15, pady=(0, 12))

    def _apply_filters(self, *args):
        """Apply filters and refresh the data table."""
        # Get filter values
        emotion = self.emotion_filter.get()

        person_min = None
        person_max = None
        try:
            if self.person_min.get():
                person_min = int(self.person_min.get())
            if self.person_max.get():
                person_max = int(self.person_max.get())
        except ValueError:
            pass

        keyword = self.keyword_search.get().strip()

        # Get filtered data
        db = self.scanner.get_database()
        self.current_filtered_data = db.get_filtered_metadata(
            emotion_filter=emotion if emotion != "All" else None,
            person_count_min=person_min,
            person_count_max=person_max,
            keyword_search=keyword if keyword else None
        )

        # Clear existing data rows (keep header)
        for widget in self.filtered_data_scroll.winfo_children()[1:]:
            widget.destroy()

        # Display filtered records
        for i, record in enumerate(self.current_filtered_data[:100], start=1):
            self._create_filtered_data_row(i, record)

    def _create_filtered_data_row(self, row_num: int, record: dict):
        """Create a filtered data row with thumbnail and click functionality."""
        filepath = record.get('filepath', '')

        row_frame = ctk.CTkFrame(
            self.filtered_data_scroll,
            fg_color="#2B2B2B" if row_num % 2 == 0 else "#1E1E1E",
            corner_radius=3
        )
        row_frame.grid(row=row_num, column=0, padx=5, pady=2, sticky="ew")
        row_frame.grid_columnconfigure((1, 2, 3, 4, 5), weight=1)
        row_frame.grid_columnconfigure(0, weight=0, minsize=80)

        # Make the entire row clickable
        row_frame.bind("<Button-1>", lambda e: self._open_file(filepath))

        # Thumbnail
        thumbnail_label = self._create_thumbnail_widget(row_frame, record)
        thumbnail_label.grid(row=0, column=0, padx=8, pady=6, sticky="w")
        thumbnail_label.bind("<Button-1>", lambda e: self._open_file(filepath))

        # Filename
        filename_label = ctk.CTkLabel(
            row_frame,
            text=record.get('filename', 'N/A')[:25],
            font=ctk.CTkFont(size=10),
            anchor="w",
            cursor="hand2"
        )
        filename_label.grid(row=0, column=1, padx=8, pady=6, sticky="w")
        filename_label.bind("<Button-1>", lambda e: self._open_file(filepath))

        # Date/Time
        datetime_label = ctk.CTkLabel(
            row_frame,
            text=record.get('date_time_original', 'N/A')[:16],
            font=ctk.CTkFont(size=10),
            anchor="w",
            cursor="hand2"
        )
        datetime_label.grid(row=0, column=2, padx=8, pady=6, sticky="w")
        datetime_label.bind("<Button-1>", lambda e: self._open_file(filepath))

        # Person Count
        person_label = ctk.CTkLabel(
            row_frame,
            text=str(record.get('person_count', 0)),
            font=ctk.CTkFont(size=10),
            anchor="w",
            cursor="hand2"
        )
        person_label.grid(row=0, column=3, padx=8, pady=6, sticky="w")
        person_label.bind("<Button-1>", lambda e: self._open_file(filepath))

        # Emotion
        emotion_label = ctk.CTkLabel(
            row_frame,
            text=record.get('emotion_sentiment', 'N/A')[:15],
            font=ctk.CTkFont(size=10),
            anchor="w",
            cursor="hand2"
        )
        emotion_label.grid(row=0, column=4, padx=8, pady=6, sticky="w")
        emotion_label.bind("<Button-1>", lambda e: self._open_file(filepath))

        # Keywords
        keywords = record.get('object_keywords', 'N/A')[:30]
        keywords_label = ctk.CTkLabel(
            row_frame,
            text=keywords,
            font=ctk.CTkFont(size=10),
            anchor="w",
            cursor="hand2"
        )
        keywords_label.grid(row=0, column=5, padx=8, pady=6, sticky="w")
        keywords_label.bind("<Button-1>", lambda e: self._open_file(filepath))

    def _create_thumbnail_widget(self, parent, record: dict):
        """Create a thumbnail widget for the record."""
        thumbnail_path = record.get('thumbnail_path')

        # Default placeholder image (gray square)
        placeholder_img = Image.new('RGB', (64, 64), color='#3B3B3B')

        try:
            if thumbnail_path and os.path.exists(thumbnail_path):
                # Load the actual thumbnail
                pil_image = Image.open(thumbnail_path)
            else:
                # Use placeholder
                pil_image = placeholder_img
        except Exception as e:
            print(f"Error loading thumbnail: {e}")
            pil_image = placeholder_img

        # Create CTkImage
        ctk_image = ctk.CTkImage(
            light_image=pil_image,
            dark_image=pil_image,
            size=(64, 64)
        )

        # Create label with image
        thumbnail_label = ctk.CTkLabel(
            parent,
            image=ctk_image,
            text="",
            cursor="hand2"
        )
        thumbnail_label.image = ctk_image  # Keep a reference

        return thumbnail_label

    def _open_file(self, filepath: str):
        """Open the media file with the default system viewer."""
        if not filepath or not os.path.exists(filepath):
            messagebox.showerror(
                "File Not Found",
                f"The file does not exist:\n{filepath}"
            )
            return

        try:
            # Use os.startfile on Windows to open with default application
            os.startfile(filepath)
        except Exception as e:
            messagebox.showerror(
                "Error Opening File",
                f"Failed to open file:\n{filepath}\n\nError: {str(e)}"
            )

    def _export_data(self):
        """Export data to CSV file."""
        # Ask user what to export
        dialog = ExportDialog(self)
        self.wait_window(dialog)

        if not hasattr(dialog, 'export_choice'):
            return

        # Get file path
        filepath = filedialog.asksaveasfilename(
            title="Save CSV File",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not filepath:
            return

        # Export data
        db = self.scanner.get_database()

        if dialog.export_choice == "all":
            success = db.export_to_csv(filepath)
            count = db.get_record_count()
        else:  # filtered
            success = db.export_to_csv(filepath, self.current_filtered_data)
            count = len(self.current_filtered_data)

        if success:
            messagebox.showinfo(
                "Export Successful",
                f"Successfully exported {count} records to:\n{filepath}"
            )
        else:
            messagebox.showerror(
                "Export Failed",
                "Failed to export data. Please check the file path and try again."
            )


class ExportDialog(ctk.CTkToplevel):
    """Dialog for choosing export options."""

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Export Options")
        self.geometry("400x200")
        self.resizable(False, False)

        # Make modal
        self.transient(parent)
        self.grab_set()

        self.export_choice = None

        self._build_ui()

    def _build_ui(self):
        """Build the export dialog UI."""
        main_frame = ctk.CTkFrame(self, corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            main_frame,
            text="What would you like to export?",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title.pack(pady=(15, 20))

        all_btn = ctk.CTkButton(
            main_frame,
            text="Export All Records",
            command=lambda: self._set_choice("all"),
            width=200,
            height=40,
            font=ctk.CTkFont(size=13)
        )
        all_btn.pack(pady=10)

        filtered_btn = ctk.CTkButton(
            main_frame,
            text="Export Filtered Records Only",
            command=lambda: self._set_choice("filtered"),
            width=200,
            height=40,
            font=ctk.CTkFont(size=13)
        )
        filtered_btn.pack(pady=10)

    def _set_choice(self, choice: str):
        """Set the export choice and close dialog."""
        self.export_choice = choice
        self.destroy()


class TesseractSetupDialog(ctk.CTkToplevel):
    """Dialog for Tesseract OCR setup instructions."""

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Tesseract OCR Setup Required")
        self.geometry("700x600")
        self.resizable(False, False)

        # Make dialog modal
        self.transient(parent)
        self.grab_set()

        self._build_ui()

    def _build_ui(self):
        """Build the setup dialog UI."""
        # Main frame
        main_frame = ctk.CTkFrame(self, corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="⚠️ Step 1: Install Tesseract OCR Engine",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFA500"
        )
        title_label.pack(pady=(20, 10))

        # Instructions
        instructions = """
MediaVault Scanner requires Tesseract OCR to extract text from images and videos.

INSTALLATION INSTRUCTIONS:

A. Download Tesseract for Windows:
   • Visit the official Tesseract installer page:
     https://github.com/UB-Mannheim/tesseract/wiki

   • Download the latest Windows installer (tesseract-ocr-w64-setup-*.exe)

   • Run the installer and follow the installation wizard
   • Note the installation path (default: C:\\Program Files\\Tesseract-OCR)

B. Add Tesseract to Windows System PATH (CRITICAL):
   1. Open Windows Settings → System → About
   2. Click "Advanced system settings"
   3. Click "Environment Variables"
   4. Under "System variables", find and select "Path"
   5. Click "Edit"
   6. Click "New"
   7. Add the Tesseract installation path:
      C:\\Program Files\\Tesseract-OCR
   8. Click "OK" on all dialogs
   9. RESTART this application for changes to take effect

C. Alternative: Specify Tesseract Path Manually:
   • If you prefer not to modify the system PATH, you can specify
     the Tesseract executable path below.
   • The path should point to tesseract.exe, for example:
     C:\\Program Files\\Tesseract-OCR\\tesseract.exe

VERIFICATION:
   • After installation, restart this application
   • MediaVault will automatically detect Tesseract if it's in the PATH
   • OCR features will be enabled once Tesseract is detected
        """

        instructions_text = ctk.CTkTextbox(
            main_frame,
            font=ctk.CTkFont(size=12),
            wrap="word",
            height=350
        )
        instructions_text.pack(fill="both", expand=True, padx=20, pady=10)
        instructions_text.insert("1.0", instructions)
        instructions_text.configure(state="disabled")

        # Manual path entry
        path_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        path_frame.pack(fill="x", padx=20, pady=10)

        path_label = ctk.CTkLabel(
            path_frame,
            text="Tesseract Path (Optional):",
            font=ctk.CTkFont(size=12)
        )
        path_label.pack(side="left", padx=(0, 10))

        self.path_entry = ctk.CTkEntry(path_frame, width=300)
        self.path_entry.pack(side="left", padx=(0, 10))

        browse_btn = ctk.CTkButton(
            path_frame,
            text="Browse",
            command=self._browse_tesseract,
            width=100
        )
        browse_btn.pack(side="left")

        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(10, 20))

        save_btn = ctk.CTkButton(
            button_frame,
            text="Save Path & Continue",
            command=self._save_path,
            width=180,
            fg_color="#2B7A0B",
            hover_color="#1F5A08"
        )
        save_btn.pack(side="left", padx=(0, 10))

        skip_btn = ctk.CTkButton(
            button_frame,
            text="Skip for Now",
            command=self.destroy,
            width=150,
            fg_color="#666666",
            hover_color="#555555"
        )
        skip_btn.pack(side="left")

    def _browse_tesseract(self):
        """Browse for Tesseract executable."""
        filepath = filedialog.askopenfilename(
            title="Select Tesseract Executable",
            filetypes=[("Executable Files", "*.exe"), ("All Files", "*.*")]
        )
        if filepath:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, filepath)

    def _save_path(self):
        """Save the Tesseract path."""
        path = self.path_entry.get()
        if path and os.path.exists(path):
            Config.set_tesseract_path(path)
            self.destroy()
        elif path:
            # Show error
            error_label = ctk.CTkLabel(
                self,
                text="Invalid path! File does not exist.",
                text_color="#FF0000"
            )
            error_label.place(relx=0.5, rely=0.95, anchor="center")
            self.after(3000, error_label.destroy)


def main():
    """Main entry point for the application."""
    app = MediaVaultApp()
    app.mainloop()


if __name__ == "__main__":
    main()

