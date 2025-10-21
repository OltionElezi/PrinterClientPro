"""
Windows Printer Client - Desktop GUI Application
A graphical interface for the printer client with real-time logs and configuration
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import socketio
import threading
import json
import logging
from datetime import datetime
from printer_handler import PrinterHandler
from config import Config
import os
import tempfile
import webbrowser

class PrinterClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Print Client Pro")
        self.root.geometry("1200x800")

        # Make window resizable
        self.root.resizable(True, True)

        # Set minimum size
        self.root.minsize(1000, 600)

        # Keep window in taskbar but use custom styling
        # We'll style over the default title bar instead of removing it
        self.root.configure(bg='#0F172A')

        # Set icon (optional)
        try:
            self.root.iconbitmap('printer.ico')
        except:
            pass

        self.config = Config()
        self.sio = socketio.Client(logger=False, engineio_logger=False)
        self.printer_handler = PrinterHandler()
        self.connected = False

        # Load printer settings from config file
        self.printer_settings = self.load_printer_settings()

        # Setup GUI
        self.setup_gui()
        self.setup_logging()
        self.setup_event_handlers()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Auto-connect on startup (after a short delay to let GUI finish loading)
        self.root.after(500, self.auto_connect_on_startup)

    def setup_gui(self):
        """Setup the GUI layout"""

        # Modern color scheme
        self.colors = {
            'bg': '#0F172A',          # Slate-900 (dark background)
            'bg_light': '#1E293B',    # Slate-800 (lighter bg)
            'bg_dark': '#020617',     # Slate-950 (darker bg)
            'accent': '#6366F1',      # Indigo-500 (primary)
            'success': '#10B981',     # Emerald-500
            'danger': '#EF4444',      # Red-500
            'warning': '#F59E0B',     # Amber-500
            'text': '#F1F5F9',        # Slate-100
            'text_dim': '#94A3B8'     # Slate-400
        }

        self.root.configure(bg=self.colors['bg'])

        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Left panel - Compact Navigation
        left_panel = tk.Frame(main_container, bg=self.colors['bg'], width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), pady=0)
        left_panel.pack_propagate(False)

        # Variables for config
        self.url_var = tk.StringVar(value=self.config.SOCKET_URL)
        self.nipt_var = tk.StringVar(value=self.config.NIPT)
        self.username_var = tk.StringVar(value=self.config.USERNAME)
        self.session_var = tk.StringVar(value=self.config.SESSION_ID)
        self.pdf_converter_var = tk.StringVar(value=self.config.PDF_CONVERTER)

        # Configuration button (toggle)
        self.config_visible = False
        config_toggle_btn = tk.Button(
            left_panel,
            text="⚙️ Configuration",
            command=self.toggle_config_panel,
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            font=("Segoe UI", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            anchor='w',
            padx=15
        )
        config_toggle_btn.pack(fill=tk.X, pady=(10, 5), ipady=10)

        # Configuration panel container (initially hidden)
        self.config_panel_container = tk.Frame(left_panel, bg=self.colors['bg_light'])

        # Create canvas for scrolling
        config_canvas = tk.Canvas(self.config_panel_container, bg=self.colors['bg_light'], highlightthickness=0, height=300)
        config_scrollbar = tk.Scrollbar(self.config_panel_container, orient="vertical", command=config_canvas.yview)

        # Scrollable frame inside canvas
        self.config_panel = tk.Frame(config_canvas, bg=self.colors['bg_light'])

        # Configure canvas scrolling
        self.config_panel.bind(
            "<Configure>",
            lambda e: config_canvas.configure(scrollregion=config_canvas.bbox("all"))
        )

        config_canvas.create_window((0, 0), window=self.config_panel, anchor="nw")
        config_canvas.configure(yscrollcommand=config_scrollbar.set)

        # Pack scrollbar and canvas
        config_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        config_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            config_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        config_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Server URL
        tk.Label(self.config_panel, text="Socket Server URL:", anchor="w", bg=self.colors['bg_light'], fg=self.colors['text_dim'], font=("Segoe UI", 9)).pack(fill=tk.X, pady=(10, 2), padx=10)
        tk.Entry(self.config_panel, textvariable=self.url_var, bg=self.colors['bg'], fg=self.colors['text'], insertbackground=self.colors['text'], relief=tk.FLAT, font=("Segoe UI", 9)).pack(fill=tk.X, pady=(0, 10), ipady=6, ipadx=8, padx=10)

        # NIPT
        tk.Label(self.config_panel, text="NIPT (Company ID):", anchor="w", bg=self.colors['bg_light'], fg=self.colors['text_dim'], font=("Segoe UI", 9)).pack(fill=tk.X, pady=(0, 2), padx=10)
        tk.Entry(self.config_panel, textvariable=self.nipt_var, bg=self.colors['bg'], fg=self.colors['warning'], insertbackground=self.colors['warning'], relief=tk.FLAT, font=("Segoe UI", 10, "bold")).pack(fill=tk.X, pady=(0, 10), ipady=6, ipadx=8, padx=10)

        # Username
        tk.Label(self.config_panel, text="Username:", anchor="w", bg=self.colors['bg_light'], fg=self.colors['text_dim'], font=("Segoe UI", 9)).pack(fill=tk.X, pady=(0, 2), padx=10)
        tk.Entry(self.config_panel, textvariable=self.username_var, bg=self.colors['bg'], fg=self.colors['text'], insertbackground=self.colors['text'], relief=tk.FLAT, font=("Segoe UI", 9)).pack(fill=tk.X, pady=(0, 10), ipady=6, ipadx=8, padx=10)

        # Session ID
        tk.Label(self.config_panel, text="Session ID:", anchor="w", bg=self.colors['bg_light'], fg=self.colors['text_dim'], font=("Segoe UI", 9)).pack(fill=tk.X, pady=(0, 2), padx=10)
        tk.Entry(self.config_panel, textvariable=self.session_var, bg=self.colors['bg'], fg=self.colors['text'], insertbackground=self.colors['text'], relief=tk.FLAT, font=("Segoe UI", 9)).pack(fill=tk.X, pady=(0, 10), ipady=6, ipadx=8, padx=10)

        # Font Scale Configuration
        tk.Label(self.config_panel, text="Font Scale (for ReportLab):", anchor="w", bg=self.colors['bg_light'], fg=self.colors['text_dim'], font=("Segoe UI", 9)).pack(fill=tk.X, pady=(0, 2), padx=10)

        font_scale_frame = tk.Frame(self.config_panel, bg=self.colors['bg_light'])
        font_scale_frame.pack(fill=tk.X, pady=(0, 5), padx=10)

        # Font scale variable
        self.font_scale_var = tk.DoubleVar(value=0.8)

        # Load font scale from config
        try:
            from config import Config
            self.font_scale_var.set(Config.FONT_SCALE)
        except:
            pass

        # Label showing current value
        self.font_scale_label = tk.Label(font_scale_frame, text=f"{int(self.font_scale_var.get() * 100)}%",
                                         bg=self.colors['bg'], fg=self.colors['text'],
                                         font=("Segoe UI", 9, "bold"), width=5)
        self.font_scale_label.pack(side=tk.RIGHT, padx=(5, 0))

        # Slider
        font_scale_slider = tk.Scale(font_scale_frame, from_=0.5, to=1.5, resolution=0.05,
                                     orient=tk.HORIZONTAL, variable=self.font_scale_var,
                                     bg=self.colors['bg'], fg=self.colors['text'],
                                     highlightthickness=0, troughcolor=self.colors['bg_dark'],
                                     activebackground=self.colors['accent'],
                                     command=self.update_font_scale_label)
        font_scale_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Description
        tk.Label(self.config_panel, text="↑ 50% = smaller fonts, 150% = larger fonts",
                anchor="w", bg=self.colors['bg_light'], fg=self.colors['text_dim'],
                font=("Segoe UI", 8, "italic")).pack(fill=tk.X, pady=(0, 10), padx=10)

        # PDF Converter Selection
        tk.Label(self.config_panel, text="PDF Converter:", anchor="w", bg=self.colors['bg_light'], fg=self.colors['text_dim'], font=("Segoe UI", 9)).pack(fill=tk.X, pady=(0, 5), padx=10)

        # First row of converters
        pdf_converter_frame1 = tk.Frame(self.config_panel, bg=self.colors['bg_light'])
        pdf_converter_frame1.pack(fill=tk.X, pady=(0, 3), padx=10)

        # wkhtmltopdf button (RECOMMENDED)
        wkhtmltopdf_btn = tk.Button(
            pdf_converter_frame1,
            text="wkhtmltopdf ⭐",
            command=lambda: self.select_pdf_converter('wkhtmltopdf'),
            bg=self.colors['accent'] if self.pdf_converter_var.get() == 'wkhtmltopdf' else self.colors['bg'],
            fg=self.colors['text'],
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=self.colors['accent']
        )
        wkhtmltopdf_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 3), ipady=6)
        self.wkhtmltopdf_btn = wkhtmltopdf_btn

        # ReportLab button
        reportlab_btn = tk.Button(
            pdf_converter_frame1,
            text="ReportLab",
            command=lambda: self.select_pdf_converter('reportlab'),
            bg=self.colors['accent'] if self.pdf_converter_var.get() == 'reportlab' else self.colors['bg'],
            fg=self.colors['text'],
            font=("Segoe UI", 9),
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=self.colors['accent']
        )
        reportlab_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
        self.reportlab_btn = reportlab_btn

        # Second row of converters
        pdf_converter_frame2 = tk.Frame(self.config_panel, bg=self.colors['bg_light'])
        pdf_converter_frame2.pack(fill=tk.X, pady=(0, 10), padx=10)

        # WeasyPrint button
        weasyprint_btn = tk.Button(
            pdf_converter_frame2,
            text="WeasyPrint",
            command=lambda: self.select_pdf_converter('weasyprint'),
            bg=self.colors['accent'] if self.pdf_converter_var.get() == 'weasyprint' else self.colors['bg'],
            fg=self.colors['text'],
            font=("Segoe UI", 9),
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=self.colors['accent']
        )
        weasyprint_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 3), ipady=6)
        self.weasyprint_btn = weasyprint_btn

        # SumatraPDF button
        sumatrapdf_btn = tk.Button(
            pdf_converter_frame2,
            text="SumatraPDF",
            command=lambda: self.select_pdf_converter('sumatrapdf'),
            bg=self.colors['accent'] if self.pdf_converter_var.get() == 'sumatrapdf' else self.colors['bg'],
            fg=self.colors['text'],
            font=("Segoe UI", 9),
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=self.colors['accent']
        )
        sumatrapdf_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
        self.sumatrapdf_btn = sumatrapdf_btn

        # Save button
        save_btn = tk.Button(self.config_panel, text="💾 Save", command=self.save_config,
                            bg=self.colors['accent'], fg=self.colors['text'], font=("Segoe UI", 10, "bold"),
                            relief=tk.FLAT, cursor="hand2", activebackground="#818CF8")
        save_btn.pack(fill=tk.X, pady=(5, 15), ipady=8, padx=10)

        # Connection status
        status_frame = tk.LabelFrame(left_panel, text="  Connection Status  ", font=("Segoe UI", 10, "bold"),
                                     bg=self.colors['bg_light'], fg=self.colors['text'], relief=tk.FLAT)
        status_frame.pack(fill=tk.X, pady=(10, 0))

        self.status_indicator = tk.Label(status_frame, text="●", font=("Arial", 28), fg=self.colors['danger'], bg=self.colors['bg_light'])
        self.status_indicator.pack(pady=(10, 5))

        self.status_label = tk.Label(status_frame, text="Disconnected", font=("Segoe UI", 10, "bold"), bg=self.colors['bg_light'], fg=self.colors['text_dim'])
        self.status_label.pack()

        self.client_id_label = tk.Label(status_frame, text="", font=("Segoe UI", 8), fg=self.colors['text_dim'], bg=self.colors['bg_light'])
        self.client_id_label.pack(pady=(2, 10))

        # Connect/Disconnect button
        self.connect_btn = tk.Button(
            left_panel,
            text="🔌 Connect",
            command=self.toggle_connection,
            bg=self.colors['success'],
            fg=self.colors['text'],
            font=("Segoe UI", 11, "bold"),
            height=2,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#059669"
        )
        self.connect_btn.pack(fill=tk.X, pady=(15, 8), ipady=5)

        # Test print button
        self.test_btn = tk.Button(
            left_panel,
            text="🖨️ Test Print",
            command=self.test_print,
            bg=self.colors['warning'],
            fg=self.colors['text'],
            font=("Segoe UI", 10, "bold"),
            state=tk.DISABLED,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#D97706"
        )
        self.test_btn.pack(fill=tk.X, pady=(0, 5), ipady=6)

        # Right panel - Logs
        right_panel = tk.Frame(main_container, bg=self.colors['bg'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Statistics cards at top
        stats_container = tk.Frame(right_panel, bg=self.colors['bg'])
        stats_container.pack(fill=tk.X, pady=(0, 15))

        # Create modern stat cards
        self.stat_cards = {}
        stats = [
            ('prints', 'Total Prints', '0', self.colors['success']),
            ('errors', 'Errors', '0', self.colors['danger']),
            ('queue', 'Queue', '0', self.colors['warning'])
        ]

        for i, (key, label, value, color) in enumerate(stats):
            card = tk.Frame(stats_container, bg=self.colors['bg_light'], relief=tk.FLAT)
            card.grid(row=0, column=i, padx=8, sticky='ew', ipady=12, ipadx=15)
            stats_container.grid_columnconfigure(i, weight=1)

            tk.Label(
                card,
                text=label,
                font=("Segoe UI", 9),
                bg=self.colors['bg_light'],
                fg=self.colors['text_dim']
            ).pack(anchor='w', padx=12, pady=(8, 2))

            value_label = tk.Label(
                card,
                text=value,
                font=("Segoe UI", 24, "bold"),
                bg=self.colors['bg_light'],
                fg=color
            )
            value_label.pack(anchor='w', padx=12, pady=(0, 8))
            self.stat_cards[key] = value_label

        # View toggle buttons
        view_toggle_frame = tk.Frame(right_panel, bg=self.colors['bg'])
        view_toggle_frame.pack(fill=tk.X, pady=(0, 10))

        self.console_btn = tk.Button(
            view_toggle_frame,
            text="📋 Console Log",
            command=lambda: self.switch_view('console'),
            bg=self.colors['accent'],
            fg=self.colors['text'],
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#818CF8"
        )
        self.console_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 3), ipady=8)

        self.queue_btn = tk.Button(
            view_toggle_frame,
            text="📦 Queue",
            command=lambda: self.switch_view('queue'),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dim'],
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#1E293B"
        )
        self.queue_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(3, 3), ipady=8)

        self.printers_btn = tk.Button(
            view_toggle_frame,
            text="🖨️ Printers",
            command=lambda: self.switch_view('printers'),
            bg=self.colors['bg_light'],
            fg=self.colors['text_dim'],
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#1E293B"
        )
        self.printers_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(3, 0), ipady=8)

        # Container for both views
        content_container = tk.Frame(right_panel, bg=self.colors['bg'])
        content_container.pack(fill=tk.BOTH, expand=True)

        # Console Log View
        self.console_frame = tk.LabelFrame(
            content_container,
            text="  📋 Activity Log  ",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            relief=tk.FLAT,
            borderwidth=2
        )
        self.console_frame.pack(fill=tk.BOTH, expand=True)

        self.log_text = scrolledtext.ScrolledText(
            self.console_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief=tk.FLAT,
            borderwidth=0
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Clear log button
        clear_btn = tk.Button(
            self.console_frame,
            text="🗑️ Clear Log",
            command=self.clear_log,
            bg=self.colors['bg'],
            fg=self.colors['text_dim'],
            font=("Segoe UI", 9),
            relief=tk.FLAT,
            cursor="hand2"
        )
        clear_btn.pack(pady=8)

        # Queue View (initially hidden)
        self.queue_frame = tk.LabelFrame(
            content_container,
            text="  📦 Print Queue  ",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            relief=tk.FLAT,
            borderwidth=2
        )

        # Queue content area
        queue_scroll = tk.Frame(self.queue_frame, bg=self.colors['bg_light'])
        queue_scroll.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Canvas for scrollable queue
        self.queue_canvas = tk.Canvas(queue_scroll, bg=self.colors['bg_light'], highlightthickness=0)
        queue_scrollbar = tk.Scrollbar(queue_scroll, orient=tk.VERTICAL, command=self.queue_canvas.yview)
        self.queue_content = tk.Frame(self.queue_canvas, bg=self.colors['bg_light'])

        self.queue_canvas.configure(yscrollcommand=queue_scrollbar.set)

        queue_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.queue_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.queue_canvas.create_window((0, 0), window=self.queue_content, anchor='nw')

        self.queue_content.bind('<Configure>', lambda e: self.queue_canvas.configure(scrollregion=self.queue_canvas.bbox('all')))

        # Enable mouse wheel scrolling for queue
        def _on_queue_mousewheel(event):
            self.queue_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.queue_canvas.bind("<Enter>", lambda _: self.queue_canvas.bind_all("<MouseWheel>", _on_queue_mousewheel))
        self.queue_canvas.bind("<Leave>", lambda _: self.queue_canvas.unbind_all("<MouseWheel>"))

        # Queue action buttons
        queue_actions = tk.Frame(self.queue_frame, bg=self.colors['bg'])
        queue_actions.pack(fill=tk.X, padx=8, pady=8)

        refresh_queue_btn = tk.Button(
            queue_actions,
            text="🔄 Refresh",
            command=self.refresh_queue_display,
            bg=self.colors['accent'],
            fg=self.colors['text'],
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            cursor="hand2"
        )
        refresh_queue_btn.pack(side=tk.LEFT, padx=(0, 5), ipady=6, ipadx=10)

        clear_queue_btn = tk.Button(
            queue_actions,
            text="🗑️ Clear All",
            command=self.clear_all_queue,
            bg=self.colors['danger'],
            fg=self.colors['text'],
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            cursor="hand2"
        )
        clear_queue_btn.pack(side=tk.LEFT, padx=(0, 5), ipady=6, ipadx=10)

        # Printers Configuration View (initially hidden)
        self.printers_frame = tk.LabelFrame(
            content_container,
            text="  🖨️ Printer Configuration  ",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            relief=tk.FLAT,
            borderwidth=2
        )

        # Printers list area
        printers_scroll = tk.Frame(self.printers_frame, bg=self.colors['bg_light'])
        printers_scroll.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Canvas for scrollable printers
        self.printers_canvas = tk.Canvas(printers_scroll, bg=self.colors['bg_light'], highlightthickness=0)
        printers_scrollbar = tk.Scrollbar(printers_scroll, orient=tk.VERTICAL, command=self.printers_canvas.yview)
        self.printers_content = tk.Frame(self.printers_canvas, bg=self.colors['bg_light'])

        self.printers_canvas.configure(yscrollcommand=printers_scrollbar.set)

        printers_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.printers_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.printers_canvas.create_window((0, 0), window=self.printers_content, anchor='nw')

        self.printers_content.bind('<Configure>', lambda e: self.printers_canvas.configure(scrollregion=self.printers_canvas.bbox('all')))

        # Enable mouse wheel scrolling for printers
        def _on_printers_mousewheel(event):
            self.printers_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.printers_canvas.bind("<Enter>", lambda _: self.printers_canvas.bind_all("<MouseWheel>", _on_printers_mousewheel))
        self.printers_canvas.bind("<Leave>", lambda _: self.printers_canvas.unbind_all("<MouseWheel>"))

        # Printers action buttons
        printers_actions = tk.Frame(self.printers_frame, bg=self.colors['bg'])
        printers_actions.pack(fill=tk.X, padx=8, pady=8)

        refresh_printers_btn = tk.Button(
            printers_actions,
            text="🔄 Refresh Printers",
            command=self.refresh_printers_display,
            bg=self.colors['accent'],
            fg=self.colors['text'],
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            cursor="hand2"
        )
        refresh_printers_btn.pack(side=tk.LEFT, padx=(0, 5), ipady=6, ipadx=10)

        add_printer_btn = tk.Button(
            printers_actions,
            text="➕ Add Printer",
            command=self.add_new_printer,
            bg=self.colors['success'],
            fg=self.colors['text'],
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            cursor="hand2"
        )
        add_printer_btn.pack(side=tk.LEFT, padx=(0, 5), ipady=6, ipadx=10)

        # Track current view
        self.current_view = 'console'

        self.print_count = 0
        self.error_count = 0

    def setup_logging(self):
        """Setup custom logging to display in GUI"""
        class GUILogHandler(logging.Handler):
            def __init__(self, text_widget, gui_instance):
                super().__init__()
                self.text_widget = text_widget
                self.gui = gui_instance

            def emit(self, record):
                msg = self.format(record)

                def append():
                    self.text_widget.insert(tk.END, msg + '\n')
                    self.text_widget.see(tk.END)

                    # Color coding
                    if 'ERROR' in msg:
                        self.text_widget.tag_add("error", f"{self.text_widget.index('end-2l')}", "end-1c")
                        self.text_widget.tag_config("error", foreground="#e74c3c")
                    elif 'WARNING' in msg:
                        self.text_widget.tag_add("warning", f"{self.text_widget.index('end-2l')}", "end-1c")
                        self.text_widget.tag_config("warning", foreground="#f39c12")
                    elif 'INFO' in msg:
                        self.text_widget.tag_add("info", f"{self.text_widget.index('end-2l')}", "end-1c")
                        self.text_widget.tag_config("info", foreground="#3498db")

                self.text_widget.after(0, append)

        # Setup logger
        self.logger = logging.getLogger('PrinterClientGUI')
        self.logger.setLevel(logging.INFO)

        # Add GUI handler
        gui_handler = GUILogHandler(self.log_text, self)
        gui_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                                   datefmt='%H:%M:%S'))
        self.logger.addHandler(gui_handler)

        # Also log to file (with UTF-8 encoding to support emojis)
        file_handler = logging.FileHandler('printer_client_gui.log', encoding='utf-8')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(file_handler)

        # IMPORTANT: Also capture logs from printer_handler module
        printer_handler_logger = logging.getLogger('printer_handler')
        printer_handler_logger.setLevel(logging.DEBUG)  # Capture DEBUG level too
        printer_handler_logger.addHandler(gui_handler)
        printer_handler_logger.addHandler(file_handler)

        self.logger.info("🚀 Windows Printer Client GUI started")
        self.logger.info(f"📍 Default Printer: {self.printer_handler.default_printer}")

    def setup_event_handlers(self):
        """Setup WebSocket event handlers"""

        @self.sio.event
        def connect():
            self.connected = True
            self.logger.info("✅ Successfully connected to Backend-Socket server")
            self.update_connection_status(True)

        @self.sio.event
        def connect_error(data):
            self.logger.error(f"❌ Connection failed: {data}")
            self.connected = False
            self.update_connection_status(False)

        @self.sio.event
        def disconnect():
            self.connected = False
            self.logger.warning("⚠️ Disconnected from server")
            self.update_connection_status(False)

        @self.sio.on('status')
        def on_status(data):
            self.logger.info(f"📨 Status: {data.get('message', data)}")
            if 'sid' in str(data):
                self.root.after(0, lambda: self.client_id_label.config(text=f"ID: {self.sio.sid}"))

        @self.sio.on('print_request')
        def on_print_request(data):
            self.logger.info(f"🖨️ Print request received")
            try:
                print_data = data.get('data', {})
                printer_name = data.get('printer_name', self.printer_handler.default_printer)

                self.logger.info(f"   Type: {print_data.get('type', 'text')}")
                self.logger.info(f"   Printer: {printer_name}")

                result = self.printer_handler.print_document(print_data, printer_name)

                if result:
                    self.logger.info("✅ Print job completed successfully")
                    self.print_count += 1
                    self.root.after(0, lambda: self.stat_cards['prints'].config(text=str(self.print_count)))
                else:
                    self.logger.error("❌ Print job failed")
                    self.error_count += 1
                    self.root.after(0, lambda: self.stat_cards['errors'].config(text=str(self.error_count)))

                # Update queue size
                queue_size = len(self.printer_handler.get_queue())
                self.root.after(0, lambda: self.stat_cards['queue'].config(text=str(queue_size)))

                self.sio.emit('print_response', {
                    'status': 'success' if result else 'failed',
                    'message': 'Print job sent successfully' if result else 'Print job failed',
                    'timestamp': datetime.now().isoformat(),
                    'printer': printer_name
                })

            except Exception as e:
                self.logger.error(f"❌ Error processing print: {str(e)}")
                self.error_count += 1
                self.root.after(0, lambda: self.stat_cards['errors'].config(text=str(self.error_count)))

        @self.sio.on('pos')
        def on_pos_update(data):
            self.logger.info(f"📦 POS update received")
            pos_data = data.get('pos_data', {})
            if pos_data.get('print_required'):
                self.printer_handler.print_receipt(pos_data)

        @self.sio.on('reservation')
        def on_reservation_update(data):
            self.logger.info(f"📅 Reservation update received")
            reservation_data = data.get('reservation_data', {})
            if reservation_data.get('print_required'):
                self.printer_handler.print_reservation(reservation_data)

    def update_connection_status(self, connected):
        """Update connection status indicators"""
        def update():
            if connected:
                self.status_indicator.config(fg=self.colors['success'])
                self.status_label.config(text="Connected", fg=self.colors['success'])
                self.connect_btn.config(text="🔌 Disconnect", bg=self.colors['danger'], activebackground="#DC2626")
                self.test_btn.config(state=tk.NORMAL)
                if self.sio.sid:
                    self.client_id_label.config(text=f"ID: {self.sio.sid[:12]}...")
            else:
                self.status_indicator.config(fg=self.colors['danger'])
                self.status_label.config(text="Disconnected", fg=self.colors['text_dim'])
                self.connect_btn.config(text="🔌 Connect", bg=self.colors['success'], activebackground="#059669")
                self.test_btn.config(state=tk.DISABLED)
                self.client_id_label.config(text="")

        self.root.after(0, update)

    def toggle_connection(self):
        """Connect or disconnect from server"""
        if self.connected:
            self.disconnect_from_server()
        else:
            threading.Thread(target=self.connect_to_server, daemon=True).start()

    def connect_to_server(self):
        """Connect to Backend-Socket server"""
        try:
            url = f"{self.url_var.get()}?session_id={self.session_var.get()}&username={self.username_var.get()}&nipt={self.nipt_var.get()}"

            self.logger.info(f"🔄 Connecting to {self.url_var.get()}...")
            self.sio.connect(url, transports=['websocket'])

        except Exception as e:
            self.logger.error(f"❌ Connection failed: {str(e)}")
            self.update_connection_status(False)

    def disconnect_from_server(self):
        """Disconnect from server"""
        if self.connected:
            self.sio.disconnect()
            self.logger.info("🔌 Disconnected from server")

    def auto_connect_on_startup(self):
        """Automatically connect to server on startup"""
        if not self.connected:
            self.logger.info("🔄 Auto-connecting to server on startup...")
            threading.Thread(target=self.connect_to_server, daemon=True).start()

    def toggle_config_panel(self):
        """Toggle configuration panel visibility"""
        if self.config_visible:
            self.config_panel_container.pack_forget()
            self.config_visible = False
        else:
            self.config_panel_container.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
            self.config_visible = True

    def update_font_scale_label(self, value):
        """Update font scale label when slider changes"""
        percent = int(float(value) * 100)
        self.font_scale_label.config(text=f"{percent}%")

    def select_pdf_converter(self, converter):
        """Update PDF converter selection and button colors"""
        self.pdf_converter_var.set(converter)

        # Update button colors based on selection
        self.wkhtmltopdf_btn.config(
            bg=self.colors['accent'] if converter == 'wkhtmltopdf' else self.colors['bg']
        )
        self.reportlab_btn.config(
            bg=self.colors['accent'] if converter == 'reportlab' else self.colors['bg']
        )
        self.weasyprint_btn.config(
            bg=self.colors['accent'] if converter == 'weasyprint' else self.colors['bg']
        )
        self.sumatrapdf_btn.config(
            bg=self.colors['accent'] if converter == 'sumatrapdf' else self.colors['bg']
        )

        self.logger.info(f"📄 PDF converter selected: {converter}")

    def save_config(self):
        """Save configuration to .env file"""
        try:
            import sys
            # Get the directory where the script is running (or exe location)
            if getattr(sys, 'frozen', False):
                # Running as compiled exe
                app_dir = os.path.dirname(sys.executable)
            else:
                # Running as script
                app_dir = os.path.dirname(os.path.abspath(__file__))

            env_path = os.path.join(app_dir, '.env')

            env_content = f"""# WebSocket Server Configuration
SOCKET_URL={self.url_var.get()}

# Authentication Parameters (required by Backend-Socket)
SESSION_ID={self.session_var.get()}
CLIENT_USERNAME={self.username_var.get()}
NIPT={self.nipt_var.get()}

# PDF Converter Configuration
PDF_CONVERTER={self.pdf_converter_var.get()}

# Font Size Configuration (for ReportLab renderer)
FONT_SCALE={self.font_scale_var.get()}

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=printer_client.log

# Reconnection Settings
RECONNECT_DELAY=5
MAX_RECONNECT_ATTEMPTS=0
"""

            # Write to .env file
            with open(env_path, 'w') as f:
                f.write(env_content)

            # Reload environment variables
            from dotenv import load_dotenv
            load_dotenv(env_path, override=True)

            # Update config object
            self.config.SOCKET_URL = self.url_var.get()
            self.config.SESSION_ID = self.session_var.get()
            self.config.USERNAME = self.username_var.get()
            self.config.NIPT = self.nipt_var.get()
            self.config.PDF_CONVERTER = self.pdf_converter_var.get()
            self.config.FONT_SCALE = self.font_scale_var.get()

            self.logger.info(f"💾 Configuration saved to: {env_path}")
            messagebox.showinfo("Success", f"Configuration saved successfully!\n\nFile: {env_path}")

        except Exception as e:
            self.logger.error(f"❌ Failed to save configuration: {str(e)}")
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")

    def test_print(self):
        """Send a test print"""
        try:
            printer_name = self.printer_handler.default_printer
            self.logger.info(f"🧪 Sending test print to {printer_name}...")
            test_data = {
                'type': 'text',
                'document_name': 'Test Print',
                'content': f'Test Print from GUI\n\nDate: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\nPrinter: {printer_name}\n\nConnection: Working!'
            }
            result = self.printer_handler.print_document(test_data, printer_name)

            if result:
                self.logger.info("✅ Test print sent successfully")
                self.print_count += 1
                self.stat_cards['prints'].config(text=str(self.print_count))
            else:
                self.logger.error("❌ Test print failed")
                self.error_count += 1
                self.stat_cards['errors'].config(text=str(self.error_count))

            # Update queue size
            queue_size = len(self.printer_handler.get_queue())
            self.stat_cards['queue'].config(text=str(queue_size))

        except Exception as e:
            self.logger.error(f"❌ Test print error: {str(e)}")

    def clear_log(self):
        """Clear the log display"""
        self.log_text.delete(1.0, tk.END)
        self.logger.info("🗑️ Log cleared")

    def switch_view(self, view):
        """Switch between console log, queue, and printers view"""
        # Hide all frames
        self.queue_frame.pack_forget()
        self.console_frame.pack_forget()
        self.printers_frame.pack_forget()

        # Reset all button colors
        self.console_btn.config(bg=self.colors['bg_light'], fg=self.colors['text_dim'])
        self.queue_btn.config(bg=self.colors['bg_light'], fg=self.colors['text_dim'])
        self.printers_btn.config(bg=self.colors['bg_light'], fg=self.colors['text_dim'])

        # Show selected view
        if view == 'console':
            self.console_frame.pack(fill=tk.BOTH, expand=True)
            self.console_btn.config(bg=self.colors['accent'], fg=self.colors['text'])
            self.current_view = 'console'
        elif view == 'queue':
            self.queue_frame.pack(fill=tk.BOTH, expand=True)
            self.queue_btn.config(bg=self.colors['accent'], fg=self.colors['text'])
            self.current_view = 'queue'
            self.refresh_queue_display()
        elif view == 'printers':
            self.printers_frame.pack(fill=tk.BOTH, expand=True)
            self.printers_btn.config(bg=self.colors['accent'], fg=self.colors['text'])
            self.current_view = 'printers'
            self.refresh_printers_display()

    def refresh_queue_display(self):
        """Refresh the queue display"""
        # Clear existing queue items
        for widget in self.queue_content.winfo_children():
            widget.destroy()

        # Get queue from printer handler
        queue = self.printer_handler.get_queue()

        if not queue:
            # Show empty state
            empty_label = tk.Label(
                self.queue_content,
                text="📭 Queue is empty\n\nFailed print jobs will appear here",
                font=("Segoe UI", 12),
                bg=self.colors['bg_light'],
                fg=self.colors['text_dim'],
                justify=tk.CENTER
            )
            empty_label.pack(expand=True, pady=50)
            return

        # Group queue items by printer
        queue_by_printer = {}
        for idx, item in enumerate(queue):
            printer_name = item.get('printer_name', 'Unknown')
            if printer_name not in queue_by_printer:
                queue_by_printer[printer_name] = []
            queue_by_printer[printer_name].append((idx, item))

        # Display each printer's queue
        for printer_name, items in queue_by_printer.items():
            # Printer header
            printer_header = tk.Frame(self.queue_content, bg=self.colors['bg'], pady=5)
            printer_header.pack(fill=tk.X, padx=10, pady=(10, 5))

            tk.Label(
                printer_header,
                text=f"🖨️ {printer_name}",
                font=("Segoe UI", 11, "bold"),
                bg=self.colors['bg'],
                fg=self.colors['text']
            ).pack(side=tk.LEFT)

            tk.Label(
                printer_header,
                text=f"({len(items)} pending)",
                font=("Segoe UI", 9),
                bg=self.colors['bg'],
                fg=self.colors['text_dim']
            ).pack(side=tk.LEFT, padx=(5, 0))

            # Display each queue item for this printer
            for idx, item in items:
                self.create_queue_item_widget(idx, item)

    def create_queue_item_widget(self, idx, item):
        """Create a widget for a queue item"""
        item_frame = tk.Frame(self.queue_content, bg=self.colors['bg'], relief=tk.FLAT, borderwidth=1)
        item_frame.pack(fill=tk.X, padx=20, pady=5)

        # Left side - info
        info_frame = tk.Frame(item_frame, bg=self.colors['bg'])
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)

        # Document name
        data = item.get('data', {})
        doc_name = data.get('document_name', 'Unknown Document')
        tk.Label(
            info_frame,
            text=doc_name,
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(anchor='w')

        # Timestamp
        timestamp = item.get('timestamp', datetime.now())
        time_str = timestamp.strftime('%Y-%m-%d %H:%M:%S') if isinstance(timestamp, datetime) else str(timestamp)
        tk.Label(
            info_frame,
            text=f"⏰ {time_str}",
            font=("Segoe UI", 8),
            bg=self.colors['bg'],
            fg=self.colors['text_dim']
        ).pack(anchor='w')

        # Status
        status = item.get('status', 'pending')
        if status == 'spooler':
            status_color = self.colors['accent']
            status_text = "WINDOWS SPOOLER"
        elif status == 'pending':
            status_color = self.colors['warning']
            status_text = status.upper()
        else:
            status_color = self.colors['danger']
            status_text = status.upper()

        tk.Label(
            info_frame,
            text=f"● {status_text}",
            font=("Segoe UI", 8),
            bg=self.colors['bg'],
            fg=status_color
        ).pack(anchor='w')

        # Additional info for spooler jobs
        if status == 'spooler':
            job_id = item.get('job_id', 'N/A')
            size = item.get('size', 0)
            tk.Label(
                info_frame,
                text=f"Job ID: {job_id} | Size: {size} bytes",
                font=("Segoe UI", 7),
                bg=self.colors['bg'],
                fg=self.colors['text_dim']
            ).pack(anchor='w')

        # Right side - actions
        actions_frame = tk.Frame(item_frame, bg=self.colors['bg'])
        actions_frame.pack(side=tk.RIGHT, padx=10, pady=8)

        # Different actions for spooler vs internal queue items
        if status == 'spooler':
            # For Windows spooler jobs, only show cancel button
            cancel_btn = tk.Button(
                actions_frame,
                text="❌ Cancel Job",
                command=lambda i=item: self.cancel_spooler_job(i),
                bg=self.colors['danger'],
                fg=self.colors['text'],
                font=("Segoe UI", 9, "bold"),
                relief=tk.FLAT,
                cursor="hand2"
            )
            cancel_btn.pack(side=tk.LEFT, padx=2, ipady=4, ipadx=8)
        else:
            # For internal queue items, show preview, retry and delete
            show_btn = tk.Button(
                actions_frame,
                text="👁️ Show",
                command=lambda i=item: self.show_print_preview(i),
                bg=self.colors['accent'],
                fg=self.colors['text'],
                font=("Segoe UI", 9, "bold"),
                relief=tk.FLAT,
                cursor="hand2"
            )
            show_btn.pack(side=tk.LEFT, padx=2, ipady=4, ipadx=8)

            retry_btn = tk.Button(
                actions_frame,
                text="🔄 Retry",
                command=lambda i=idx: self.retry_queue_item(i),
                bg=self.colors['success'],
                fg=self.colors['text'],
                font=("Segoe UI", 9, "bold"),
                relief=tk.FLAT,
                cursor="hand2"
            )
            retry_btn.pack(side=tk.LEFT, padx=2, ipady=4, ipadx=8)

            delete_btn = tk.Button(
                actions_frame,
                text="🗑️",
                command=lambda i=idx: self.delete_queue_item(i),
                bg=self.colors['danger'],
                fg=self.colors['text'],
                font=("Segoe UI", 9, "bold"),
                relief=tk.FLAT,
                cursor="hand2"
            )
            delete_btn.pack(side=tk.LEFT, padx=2, ipady=4, ipadx=8)

    def retry_queue_item(self, idx):
        """Retry a specific queue item"""
        try:
            result = self.printer_handler.retry_queue_item(idx)
            if result:
                self.logger.info(f"✅ Queue item {idx} retried successfully")
                self.print_count += 1
                self.stat_cards['prints'].config(text=str(self.print_count))
            else:
                self.logger.error(f"❌ Failed to retry queue item {idx}")
                self.error_count += 1
                self.stat_cards['errors'].config(text=str(self.error_count))

            # Update queue size and refresh display
            queue_size = len(self.printer_handler.get_queue())
            self.stat_cards['queue'].config(text=str(queue_size))
            self.refresh_queue_display()

        except Exception as e:
            self.logger.error(f"❌ Error retrying queue item: {str(e)}")

    def delete_queue_item(self, idx):
        """Delete a specific queue item"""
        try:
            queue = self.printer_handler.get_queue()
            if 0 <= idx < len(queue):
                queue.pop(idx)
                self.logger.info(f"🗑️ Removed queue item {idx}")
                queue_size = len(queue)
                self.stat_cards['queue'].config(text=str(queue_size))
                self.refresh_queue_display()
        except Exception as e:
            self.logger.error(f"❌ Error deleting queue item: {str(e)}")

    def clear_all_queue(self):
        """Clear all items from the queue"""
        if messagebox.askyesno("Clear Queue", "Are you sure you want to clear all queued items?"):
            self.printer_handler.clear_queue()
            self.logger.info("🗑️ Queue cleared")
            self.stat_cards['queue'].config(text='0')
            self.refresh_queue_display()

    def cancel_spooler_job(self, item):
        """Cancel a job in Windows print spooler"""
        try:
            printer_name = item.get('printer_name')
            job_id = item.get('job_id')
            doc_name = item.get('data', {}).get('document_name', 'Unknown')

            if messagebox.askyesno("Cancel Job", f"Cancel job '{doc_name}' (ID: {job_id})?"):
                result = self.printer_handler.cancel_spooler_job(printer_name, job_id)
                if result:
                    self.logger.info(f"✅ Cancelled spooler job {job_id}")
                else:
                    self.logger.error(f"❌ Failed to cancel spooler job {job_id}")

                # Refresh the display
                self.refresh_queue_display()
                # Update queue count
                queue_size = len(self.printer_handler.get_queue())
                self.stat_cards['queue'].config(text=str(queue_size))

        except Exception as e:
            self.logger.error(f"❌ Error cancelling spooler job: {str(e)}")

    def show_html_in_browser(self, item):
        """Show HTML content in default browser"""
        try:
            data = item.get('data', {})
            doc_name = data.get('document_name', 'Unknown Document')
            html_content = data.get('html', '') or data.get('content', '')

            if not html_content:
                messagebox.showwarning("No Content", "No HTML content found in this print job")
                return

            # Create temp HTML file
            temp_file = os.path.join(tempfile.gettempdir(), f"{doc_name.replace(' ', '_')}.html")

            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            # Open in default browser
            webbrowser.open(f'file:///{temp_file}')
            self.logger.info(f"📄 Opened preview in browser: {temp_file}")

        except Exception as e:
            self.logger.error(f"❌ Error opening HTML preview: {str(e)}")
            messagebox.showerror("Preview Error", f"Could not open HTML preview: {str(e)}")

    def refresh_printers_display(self):
        """Refresh the printers configuration display"""
        # Clear existing printer items
        for widget in self.printers_content.winfo_children():
            widget.destroy()

        # Get all available printers
        printers = self.printer_handler.get_available_printers()

        if not printers:
            # Show empty state
            empty_label = tk.Label(
                self.printers_content,
                text="⚠️ No printers found\n\nPlease install printers on your system",
                font=("Segoe UI", 12),
                bg=self.colors['bg_light'],
                fg=self.colors['text_dim'],
                justify=tk.CENTER
            )
            empty_label.pack(expand=True, pady=50)
            return

        # Display each printer
        for printer_info in printers:
            printer_name = printer_info['name'] if isinstance(printer_info, dict) else printer_info
            status = printer_info.get('status', 'Unknown') if isinstance(printer_info, dict) else 'Unknown'
            is_default = printer_info.get('is_default', False) if isinstance(printer_info, dict) else False

            self.create_printer_config_widget(printer_name, status, is_default)

    def create_printer_config_widget(self, printer_name, status, is_default):
        """Create a widget for a printer configuration"""
        # Main container with border
        container_frame = tk.Frame(self.printers_content, bg=self.colors['bg_light'], relief=tk.SOLID, borderwidth=1)
        container_frame.pack(fill=tk.X, padx=10, pady=8)

        # Header with printer name and default badge
        header_frame = tk.Frame(container_frame, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, padx=15, pady=(12, 8))

        name_label_frame = tk.Frame(header_frame, bg=self.colors['bg'])
        name_label_frame.pack(side=tk.LEFT)

        tk.Label(
            name_label_frame,
            text=f"🖨️  {printer_name}",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT)

        if is_default:
            default_badge = tk.Label(
                name_label_frame,
                text="DEFAULT",
                font=("Segoe UI", 7, "bold"),
                bg=self.colors['success'],
                fg=self.colors['text'],
                padx=6,
                pady=2
            )
            default_badge.pack(side=tk.LEFT, padx=(8, 0))

        # Status
        status_colors = {
            'Ready': self.colors['success'],
            'Offline': self.colors['danger'],
            'Error': self.colors['danger'],
            'Paused': self.colors['warning'],
            'Paper Jam': self.colors['danger'],
            'Paper Out': self.colors['warning'],
            'Not Available': self.colors['text_dim']
        }
        status_color = status_colors.get(status, self.colors['text_dim'])

        tk.Label(
            header_frame,
            text=f"● {status}",
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['bg'],
            fg=status_color
        ).pack(side=tk.RIGHT)

        # Configuration fields
        config_frame = tk.Frame(container_frame, bg=self.colors['bg'])
        config_frame.pack(fill=tk.X, padx=15, pady=8)

        # System Name (read-only)
        tk.Label(
            config_frame,
            text="System Name:",
            font=("Segoe UI", 9),
            bg=self.colors['bg'],
            fg=self.colors['text_dim'],
            anchor='w'
        ).grid(row=0, column=0, sticky='w', pady=(0, 5))

        tk.Label(
            config_frame,
            text=printer_name,
            font=("Segoe UI", 9, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            anchor='w'
        ).grid(row=0, column=1, sticky='w', padx=(10, 0), pady=(0, 5))

        # Display Name (editable)
        tk.Label(
            config_frame,
            text="Display Name:",
            font=("Segoe UI", 9),
            bg=self.colors['bg'],
            fg=self.colors['text_dim'],
            anchor='w'
        ).grid(row=1, column=0, sticky='w', pady=(0, 5))

        display_name_var = tk.StringVar(value=self.get_printer_display_name(printer_name))
        display_name_entry = tk.Entry(
            config_frame,
            textvariable=display_name_var,
            width=30,
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief=tk.FLAT,
            font=("Segoe UI", 9)
        )
        display_name_entry.grid(row=1, column=1, sticky='ew', padx=(10, 0), pady=(0, 5), ipady=4, ipadx=6)

        # Alias/Nickname (editable)
        tk.Label(
            config_frame,
            text="Alias/Nickname:",
            font=("Segoe UI", 9),
            bg=self.colors['bg'],
            fg=self.colors['text_dim'],
            anchor='w'
        ).grid(row=2, column=0, sticky='w', pady=(0, 5))

        alias_var = tk.StringVar(value=self.get_printer_alias(printer_name))
        alias_entry = tk.Entry(
            config_frame,
            textvariable=alias_var,
            width=30,
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief=tk.FLAT,
            font=("Segoe UI", 9)
        )
        alias_entry.grid(row=2, column=1, sticky='ew', padx=(10, 0), pady=(0, 5), ipady=4, ipadx=6)

        # Description (editable)
        tk.Label(
            config_frame,
            text="Description:",
            font=("Segoe UI", 9),
            bg=self.colors['bg'],
            fg=self.colors['text_dim'],
            anchor='w'
        ).grid(row=3, column=0, sticky='w', pady=(0, 5))

        description_var = tk.StringVar(value=self.get_printer_description(printer_name))
        description_entry = tk.Entry(
            config_frame,
            textvariable=description_var,
            width=30,
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief=tk.FLAT,
            font=("Segoe UI", 9)
        )
        description_entry.grid(row=3, column=1, sticky='ew', padx=(10, 0), pady=(0, 5), ipady=4, ipadx=6)

        # Location (editable)
        tk.Label(
            config_frame,
            text="Location:",
            font=("Segoe UI", 9),
            bg=self.colors['bg'],
            fg=self.colors['text_dim'],
            anchor='w'
        ).grid(row=4, column=0, sticky='w', pady=(0, 5))

        location_var = tk.StringVar(value=self.get_printer_location(printer_name))
        location_entry = tk.Entry(
            config_frame,
            textvariable=location_var,
            width=30,
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief=tk.FLAT,
            font=("Segoe UI", 9)
        )
        location_entry.grid(row=4, column=1, sticky='ew', padx=(10, 0), pady=(0, 5), ipady=4, ipadx=6)

        config_frame.columnconfigure(1, weight=1)

        # Action buttons
        actions_frame = tk.Frame(container_frame, bg=self.colors['bg'])
        actions_frame.pack(fill=tk.X, padx=15, pady=(8, 12))

        # Save button
        save_btn = tk.Button(
            actions_frame,
            text="💾 Save Settings",
            command=lambda: self.save_printer_settings(
                printer_name,
                display_name_var.get(),
                alias_var.get(),
                description_var.get(),
                location_var.get()
            ),
            bg=self.colors['success'],
            fg=self.colors['text'],
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            cursor="hand2"
        )
        save_btn.pack(side=tk.LEFT, padx=(0, 5), ipady=4, ipadx=10)

        # Set as default button
        if not is_default:
            default_btn = tk.Button(
                actions_frame,
                text="⭐ Set Default",
                command=lambda p=printer_name: self.set_default_printer(p),
                bg=self.colors['warning'],
                fg=self.colors['text'],
                font=("Segoe UI", 9, "bold"),
                relief=tk.FLAT,
                cursor="hand2"
            )
            default_btn.pack(side=tk.LEFT, padx=(0, 5), ipady=4, ipadx=10)

        # Test print button
        test_btn = tk.Button(
            actions_frame,
            text="🧪 Test Print",
            command=lambda p=printer_name: self.test_printer_direct(p),
            bg=self.colors['accent'],
            fg=self.colors['text'],
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            cursor="hand2"
        )
        test_btn.pack(side=tk.LEFT, padx=(0, 5), ipady=4, ipadx=10)

        # Printer Properties button
        properties_btn = tk.Button(
            actions_frame,
            text="⚙️ Printer Properties",
            command=lambda p=printer_name: self.open_printer_properties(p),
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            cursor="hand2"
        )
        properties_btn.pack(side=tk.LEFT, padx=(0, 5), ipady=4, ipadx=10)

    def open_printer_properties(self, printer_name):
        """Open Windows printer properties dialog"""
        try:
            import subprocess
            # Open printer properties using rundll32
            subprocess.Popen(['rundll32', 'printui.dll,PrintUIEntry', '/p', '/n', printer_name])
            self.logger.info(f"⚙️ Opening properties for: {printer_name}")
        except Exception as e:
            self.logger.error(f"❌ Error opening printer properties: {str(e)}")
            messagebox.showerror("Error", f"Could not open printer properties: {str(e)}")

    def add_new_printer(self):
        """Open Windows Add Printer dialog"""
        try:
            import subprocess
            # Open Windows Add Printer wizard
            subprocess.Popen(['rundll32', 'printui.dll,PrintUIEntry', '/il'])
            self.logger.info("🖨️ Opening Windows Add Printer wizard...")
            messagebox.showinfo("Add Printer", "Windows Add Printer wizard opened.\n\nClick 'Refresh Printers' after adding a new printer.")
        except Exception as e:
            self.logger.error(f"❌ Error opening Add Printer dialog: {str(e)}")
            messagebox.showerror("Error", f"Could not open Add Printer dialog: {str(e)}")

    def set_default_printer(self, printer_name):
        """Set a printer as the default"""
        try:
            import win32print
            win32print.SetDefaultPrinter(printer_name)
            self.printer_handler.default_printer = printer_name
            self.logger.info(f"✅ Set default printer to: {printer_name}")
            self.refresh_printers_display()
        except Exception as e:
            self.logger.error(f"❌ Error setting default printer: {str(e)}")
            messagebox.showerror("Error", f"Could not set default printer: {str(e)}")

    def test_printer_direct(self, printer_name):
        """Test a specific printer directly"""
        try:
            self.logger.info(f"🧪 Testing printer: {printer_name}")
            test_data = {
                'type': 'text',
                'document_name': 'Printer Test',
                'content': f'Printer Test\n\nPrinter: {printer_name}\nDate: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\nThis is a test print.'
            }
            result = self.printer_handler.print_document(test_data, printer_name)

            if result:
                self.logger.info(f"✅ Test print sent to {printer_name}")
                self.print_count += 1
                self.stat_cards['prints'].config(text=str(self.print_count))
            else:
                self.logger.error(f"❌ Test print failed for {printer_name}")
                self.error_count += 1
                self.stat_cards['errors'].config(text=str(self.error_count))

            # Update queue size
            queue_size = len(self.printer_handler.get_queue())
            self.stat_cards['queue'].config(text=str(queue_size))

        except Exception as e:
            self.logger.error(f"❌ Error testing printer: {str(e)}")

    def load_printer_settings(self):
        """Load printer settings from JSON file"""
        settings_file = 'printer_settings.json'
        try:
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading printer settings: {str(e)}") if hasattr(self, 'logger') else None
        return {}

    def save_printer_settings_to_file(self):
        """Save printer settings to JSON file"""
        settings_file = 'printer_settings.json'
        try:
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.printer_settings, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            self.logger.error(f"Error saving printer settings: {str(e)}")
            return False

    def get_printer_display_name(self, printer_name):
        """Get display name for printer"""
        if printer_name in self.printer_settings:
            return self.printer_settings[printer_name].get('display_name', printer_name)
        return printer_name

    def get_printer_alias(self, printer_name):
        """Get alias for printer"""
        if printer_name in self.printer_settings:
            return self.printer_settings[printer_name].get('alias', '')
        return ''

    def get_printer_description(self, printer_name):
        """Get description for printer"""
        if printer_name in self.printer_settings:
            return self.printer_settings[printer_name].get('description', '')
        return ''

    def get_printer_location(self, printer_name):
        """Get location for printer"""
        if printer_name in self.printer_settings:
            return self.printer_settings[printer_name].get('location', '')
        return ''

    def save_printer_settings(self, printer_name, display_name, alias, description, location):
        """Save settings for a specific printer"""
        try:
            # Create or update printer settings
            if printer_name not in self.printer_settings:
                self.printer_settings[printer_name] = {}

            self.printer_settings[printer_name]['display_name'] = display_name
            self.printer_settings[printer_name]['alias'] = alias
            self.printer_settings[printer_name]['description'] = description
            self.printer_settings[printer_name]['location'] = location

            # Save to file
            if self.save_printer_settings_to_file():
                self.logger.info(f"✅ Saved settings for printer: {printer_name}")
                messagebox.showinfo("Success", f"Settings saved for {display_name or printer_name}")
            else:
                messagebox.showerror("Error", "Failed to save printer settings")

        except Exception as e:
            self.logger.error(f"❌ Error saving printer settings: {str(e)}")
            messagebox.showerror("Error", f"Could not save settings: {str(e)}")

    def show_print_preview(self, item):
        """Show a preview window for the print job"""
        try:
            data = item.get('data', {})
            doc_name = data.get('document_name', 'Unknown Document')
            print_type = data.get('type', 'text')
            printer_name = item.get('printer_name', 'Unknown')
            timestamp = item.get('timestamp', datetime.now())

            # For HTML type, open in browser
            if print_type == 'html':
                self.show_html_in_browser(item)
                return

            # Create preview window for non-HTML types
            preview_window = tk.Toplevel(self.root)
            preview_window.title(f"Print Preview - {doc_name}")
            preview_window.geometry("700x600")
            preview_window.configure(bg=self.colors['bg'])

            # Header with document info
            header_frame = tk.Frame(preview_window, bg=self.colors['bg_light'], pady=15)
            header_frame.pack(fill=tk.X, padx=0, pady=0)

            tk.Label(
                header_frame,
                text=f"📄 {doc_name}",
                font=("Segoe UI", 14, "bold"),
                bg=self.colors['bg_light'],
                fg=self.colors['text']
            ).pack(pady=(5, 2))

            info_text = f"Printer: {printer_name} | Type: {print_type} | Time: {timestamp.strftime('%Y-%m-%d %H:%M:%S') if isinstance(timestamp, datetime) else str(timestamp)}"
            tk.Label(
                header_frame,
                text=info_text,
                font=("Segoe UI", 9),
                bg=self.colors['bg_light'],
                fg=self.colors['text_dim']
            ).pack(pady=(2, 5))

            # Content area
            content_frame = tk.Frame(preview_window, bg=self.colors['bg'])
            content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

            tk.Label(
                content_frame,
                text="Content Preview:",
                font=("Segoe UI", 10, "bold"),
                bg=self.colors['bg'],
                fg=self.colors['text']
            ).pack(anchor='w', pady=(0, 5))

            # Scrolled text for content
            preview_text = scrolledtext.ScrolledText(
                content_frame,
                wrap=tk.WORD,
                font=("Consolas", 10),
                bg=self.colors['bg_light'],
                fg=self.colors['text'],
                relief=tk.FLAT,
                borderwidth=0
            )
            preview_text.pack(fill=tk.BOTH, expand=True)

            # Extract and display content based on type
            if print_type == 'html':
                # Try to get HTML content from multiple possible fields
                html_content = data.get('html', '') or data.get('content', '')

                # Log what we found for debugging
                self.logger.info(f"Preview - HTML length: {len(html_content)}, Has 'html' field: {'html' in data}, Has 'content' field: {'content' in data}")

                try:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(html_content, 'html.parser')

                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()

                    # Get text
                    text = soup.get_text()

                    # Clean up text - better cleaning
                    lines = text.split('\n')
                    cleaned_lines = []
                    for line in lines:
                        line = line.strip()
                        if line:  # Only keep non-empty lines
                            cleaned_lines.append(line)

                    clean_text = '\n'.join(cleaned_lines)

                    # Show cleaned text prominently
                    preview_text.insert(tk.END, "=== Document Content (How it will print) ===\n\n", "header")

                    if clean_text:
                        preview_text.insert(tk.END, clean_text + "\n", "content")
                    else:
                        preview_text.insert(tk.END, "No readable text found in HTML\n", "error")

                    # Add styling
                    preview_text.tag_config("header", foreground="#6366F1", font=("Segoe UI", 11, "bold"))
                    preview_text.tag_config("content", foreground="#F1F5F9", font=("Segoe UI", 10))
                    preview_text.tag_config("error", foreground="#EF4444", font=("Segoe UI", 10, "italic"))

                    # Show raw HTML in collapsed section at bottom
                    preview_text.insert(tk.END, "\n" + "="*60 + "\n", "separator")
                    preview_text.insert(tk.END, "Raw HTML Source (for debugging)\n", "debug_header")
                    preview_text.insert(tk.END, "="*60 + "\n\n", "separator")
                    preview_text.insert(tk.END, html_content, "code")

                    preview_text.tag_config("separator", foreground="#94A3B8")
                    preview_text.tag_config("debug_header", foreground="#94A3B8", font=("Segoe UI", 9, "italic"))
                    preview_text.tag_config("code", foreground="#94A3B8", font=("Consolas", 8))

                except ImportError:
                    # BeautifulSoup not available
                    preview_text.insert(tk.END, "=== HTML Content ===\n\n")
                    preview_text.insert(tk.END, html_content)
                    preview_text.insert(tk.END, "\n\nNote: Install BeautifulSoup4 to see formatted preview")
                except Exception as e:
                    # Parsing failed
                    self.logger.error(f"Error parsing HTML: {str(e)}")
                    preview_text.insert(tk.END, f"=== HTML Content (parsing error) ===\n\n")
                    preview_text.insert(tk.END, f"Error: {str(e)}\n\n")
                    preview_text.insert(tk.END, html_content)

            elif print_type == 'receipt':
                receipt_data = data.get('receipt_data', {})
                preview_text.insert(tk.END, "=== RECEIPT ===\n\n")
                for key, value in receipt_data.items():
                    if key == 'items' and isinstance(value, list):
                        preview_text.insert(tk.END, f"\nItems:\n")
                        for item_obj in value:
                            preview_text.insert(tk.END, f"  - {item_obj.get('name', 'Unknown')}: ${item_obj.get('price', 0):.2f} x {item_obj.get('quantity', 1)}\n")
                    else:
                        preview_text.insert(tk.END, f"{key}: {value}\n")

            elif print_type == 'reservation':
                reservation_data = data.get('reservation_data', {})
                preview_text.insert(tk.END, "=== RESERVATION ===\n\n")
                for key, value in reservation_data.items():
                    preview_text.insert(tk.END, f"{key}: {value}\n")

            else:
                # Text content
                content = data.get('content', 'No content available')
                preview_text.insert(tk.END, content)

            preview_text.config(state=tk.DISABLED)

            # Action buttons at bottom
            button_frame = tk.Frame(preview_window, bg=self.colors['bg'])
            button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

            close_btn = tk.Button(
                button_frame,
                text="✖️ Close",
                command=preview_window.destroy,
                bg=self.colors['bg_light'],
                fg=self.colors['text'],
                font=("Segoe UI", 10, "bold"),
                relief=tk.FLAT,
                cursor="hand2"
            )
            close_btn.pack(side=tk.RIGHT, padx=(5, 0), ipady=8, ipadx=15)

        except Exception as e:
            self.logger.error(f"❌ Error showing preview: {str(e)}")
            messagebox.showerror("Preview Error", f"Could not show preview: {str(e)}")

    def on_closing(self):
        """Handle window closing"""
        if self.connected:
            if messagebox.askokcancel("Quit", "You are still connected. Do you want to quit?"):
                self.disconnect_from_server()
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    root = tk.Tk()
    app = PrinterClientGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
