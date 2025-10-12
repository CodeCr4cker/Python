import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog, colorchooser, font as tkfont
from tkinter import simpledialog
import datetime

class CompleteTkinterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Complete Tkinter Widgets & Attributes Demo - All Features")
        self.root.geometry("1100x750")
        self.root.configure(bg="#f0f0f0")
        
        # Create menubar
        self.create_menubar()
        
        # Create main canvas with scrollbar for the entire window
        main_canvas = tk.Canvas(root, bg="#f0f0f0", highlightthickness=0)
        main_scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        
        # Pack scrollbar and canvas
        main_scrollbar.pack(side="right", fill="y")
        main_canvas.pack(side="left", fill="both", expand=True)
        
        # Enable mouse wheel scrolling
        def on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        main_canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Title with anchors
        title_label = tk.Label(scrollable_frame, text="Complete Tkinter Widget & Attribute Demonstration", 
                              font=("Arial", 20, "bold"), bg="#2c3e50", fg="white", pady=15,
                              anchor="center", relief="raised", bd=5)
        title_label.pack(fill="x", padx=10, pady=10)
        
        # Sections
        self.create_basic_widgets_section(scrollable_frame)
        self.create_input_widgets_section(scrollable_frame)
        self.create_selection_widgets_section(scrollable_frame)
        self.create_display_widgets_section(scrollable_frame)
        self.create_container_widgets_section(scrollable_frame)
        self.create_advanced_widgets_section(scrollable_frame)
        self.create_messagebox_section(scrollable_frame)
        self.create_dialog_section(scrollable_frame)
        self.create_event_binding_section(scrollable_frame)
        self.create_cursor_section(scrollable_frame)
        self.create_relief_styles_section(scrollable_frame)
        self.create_anchor_section(scrollable_frame)
        self.create_bitmap_section(scrollable_frame)
        
        # Status bar at bottom
        self.create_statusbar(scrollable_frame)
    
    def create_menubar(self):
        """Create menu bar with all menu options"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=lambda: self.show_info("New File"))
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=lambda: self.show_info("Save File"))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Cut", command=lambda: self.show_info("Cut"))
        edit_menu.add_command(label="Copy", command=lambda: self.show_info("Copy"))
        edit_menu.add_command(label="Paste", command=lambda: self.show_info("Paste"))
        
        # View Menu with checkbuttons
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        self.statusbar_var = tk.BooleanVar(value=True)
        view_menu.add_checkbutton(label="Status Bar", variable=self.statusbar_var)
        view_menu.add_separator()
        
        # Submenu
        theme_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Themes", menu=theme_menu)
        theme_menu.add_command(label="Light", command=lambda: self.show_info("Light Theme"))
        theme_menu.add_command(label="Dark", command=lambda: self.show_info("Dark Theme"))
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=lambda: self.show_info("Documentation"))
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_section_frame(self, parent, title):
        """Create a styled frame for each section"""
        frame = tk.LabelFrame(parent, text=title, font=("Arial", 14, "bold"), 
                             bg="white", fg="#2c3e50", padx=15, pady=15, relief="groove", bd=3)
        frame.pack(fill="both", padx=10, pady=10, expand=True)
        return frame
    
    def create_basic_widgets_section(self, parent):
        """Section 1: Button, Label, Message with all attributes"""
        frame = self.create_section_frame(parent, "1. Basic Widgets (Button, Label, Message) - All Attributes")
        
        # Button examples with different attributes
        button_frame = tk.Frame(frame, bg="white")
        button_frame.pack(fill="x", pady=5)
        
        tk.Label(button_frame, text="Buttons with Different Attributes:", font=("Arial", 11, "bold"), bg="white").pack(anchor="w")
        
        btn_container = tk.Frame(button_frame, bg="white")
        btn_container.pack(fill="x", pady=5)
        
        btn1 = tk.Button(btn_container, text="Standard", command=lambda: self.show_info("Standard Button!"),
                        width=12, height=2)
        btn1.grid(row=0, column=0, padx=5, pady=5)
        
        btn2 = tk.Button(btn_container, text="Styled", bg="#3498db", fg="white", 
                        font=("Arial", 10, "bold"), relief="raised", bd=5,
                        activebackground="#2980b9", activeforeground="yellow",
                        command=lambda: self.show_info("Styled Button!"), width=12, height=2)
        btn2.grid(row=0, column=1, padx=5, pady=5)
        
        btn3 = tk.Button(btn_container, text="Flat Relief", relief="flat", bg="#e74c3c", fg="white",
                        width=12, height=2, command=lambda: self.show_info("Flat Button!"))
        btn3.grid(row=0, column=2, padx=5, pady=5)
        
        btn4 = tk.Button(btn_container, text="Sunken", relief="sunken", bd=3, width=12, height=2)
        btn4.grid(row=0, column=3, padx=5, pady=5)
        
        btn5 = tk.Button(btn_container, text="Groove", relief="groove", bd=4, bg="#2ecc71", fg="white",
                        width=12, height=2, command=lambda: self.show_info("Groove Button!"))
        btn5.grid(row=1, column=0, padx=5, pady=5)
        
        btn6 = tk.Button(btn_container, text="Ridge", relief="ridge", bd=4, bg="#9b59b6", fg="white",
                        width=12, height=2, command=lambda: self.show_info("Ridge Button!"))
        btn6.grid(row=1, column=1, padx=5, pady=5)
        
        btn7 = tk.Button(btn_container, text="Disabled", state="disabled", width=12, height=2)
        btn7.grid(row=1, column=2, padx=5, pady=5)
        
        btn8 = tk.Button(btn_container, text="Underline", underline=0, bg="#f39c12", fg="white",
                        width=12, height=2, command=lambda: self.show_info("Underline Button!"))
        btn8.grid(row=1, column=3, padx=5, pady=5)
        
        # Label examples with anchors
        label_frame = tk.Frame(frame, bg="white")
        label_frame.pack(fill="x", pady=10)
        
        tk.Label(label_frame, text="Labels with Different Anchors & Attributes:", 
                font=("Arial", 11, "bold"), bg="white").pack(anchor="w")
        
        tk.Label(label_frame, text="West Anchor (LEFT)", anchor="w", bg="#ecf0f1", 
                width=40, relief="solid", bd=2).pack(fill="x", pady=2)
        tk.Label(label_frame, text="Center Anchor", anchor="center", bg="#bdc3c7",
                width=40, relief="solid", bd=2, font=("Arial", 10, "bold")).pack(fill="x", pady=2)
        tk.Label(label_frame, text="East Anchor (RIGHT)", anchor="e", bg="#ecf0f1",
                width=40, relief="solid", bd=2).pack(fill="x", pady=2)
        tk.Label(label_frame, text="North Anchor (TOP)", anchor="n", bg="#95a5a6", fg="white",
                width=40, height=3, relief="solid", bd=2).pack(fill="x", pady=2)
        
        # Message widget with wraplength
        tk.Label(frame, text="Message Widget:", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(10,0))
        msg = tk.Message(frame, text="This Message widget demonstrates wraplength, width, font, and relief attributes. It automatically wraps text and can display multi-line content beautifully with various styling options.", 
                        width=500, bg="#ffffcc", relief="ridge", bd=3, font=("Arial", 10),
                        padx=10, pady=10)
        msg.pack(fill="x", pady=5)
    
    def create_input_widgets_section(self, parent):
        """Section 2: Entry, Text, ScrolledText with validation"""
        frame = self.create_section_frame(parent, "2. Input Widgets (Entry, Text, ScrolledText) - Advanced Features")
        
        # Entry widgets with different features
        tk.Label(frame, text="Entry Widgets with Features:", font=("Arial", 11, "bold"), bg="white").pack(anchor="w")
        
        entry_container = tk.Frame(frame, bg="white")
        entry_container.pack(fill="x", pady=5)
        
        tk.Label(entry_container, text="Normal Entry:", bg="white").grid(row=0, column=0, sticky="w", pady=2)
        entry1 = tk.Entry(entry_container, width=30, font=("Arial", 10))
        entry1.insert(0, "Type here...")
        entry1.grid(row=0, column=1, padx=10, pady=2)
        
        tk.Label(entry_container, text="Password Entry:", bg="white").grid(row=1, column=0, sticky="w", pady=2)
        entry2 = tk.Entry(entry_container, width=30, show="*", font=("Arial", 10))
        entry2.insert(0, "password")
        entry2.grid(row=1, column=1, padx=10, pady=2)
        
        tk.Label(entry_container, text="Read-Only Entry:", bg="white").grid(row=2, column=0, sticky="w", pady=2)
        entry3 = tk.Entry(entry_container, width=30, state="readonly", font=("Arial", 10))
        entry3.insert(0, "Cannot edit this")
        entry3.grid(row=2, column=1, padx=10, pady=2)
        
        tk.Label(entry_container, text="Justified Entry:", bg="white").grid(row=3, column=0, sticky="w", pady=2)
        entry4 = tk.Entry(entry_container, width=30, justify="center", font=("Arial", 10))
        entry4.insert(0, "Centered Text")
        entry4.grid(row=3, column=1, padx=10, pady=2)
        
        # Text widget with tags
        tk.Label(frame, text="Text Widget with Formatting (Tags):", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(10,0))
        
        text_frame = tk.Frame(frame, bg="white")
        text_frame.pack(fill="both", pady=5)
        
        text_scroll = tk.Scrollbar(text_frame)
        text_scroll.pack(side="right", fill="y")
        
        text_widget = tk.Text(text_frame, height=6, width=70, yscrollcommand=text_scroll.set, 
                             font=("Arial", 10), wrap="word", spacing1=2, spacing3=2)
        text_widget.pack(side="left", fill="both", expand=True)
        text_scroll.config(command=text_widget.yview)
        
        # Insert text with tags
        text_widget.insert("1.0", "This is normal text.\n")
        text_widget.insert("end", "This is bold text.\n", "bold")
        text_widget.insert("end", "This is colored text.\n", "color")
        text_widget.insert("end", "This is highlighted text.\n", "highlight")
        
        # Configure tags
        text_widget.tag_config("bold", font=("Arial", 10, "bold"))
        text_widget.tag_config("color", foreground="#e74c3c")
        text_widget.tag_config("highlight", background="#f39c12", foreground="white")
        
        # Add buttons for text operations
        text_btn_frame = tk.Frame(frame, bg="white")
        text_btn_frame.pack(fill="x", pady=5)
        
        tk.Button(text_btn_frame, text="Get Text", 
                 command=lambda: messagebox.showinfo("Text Content", text_widget.get("1.0", "end-1c")),
                 bg="#3498db", fg="white").pack(side="left", padx=5)
        tk.Button(text_btn_frame, text="Clear Text", 
                 command=lambda: text_widget.delete("1.0", "end"),
                 bg="#e74c3c", fg="white").pack(side="left", padx=5)
    
    def create_selection_widgets_section(self, parent):
        """Section 3: Enhanced selection widgets"""
        frame = self.create_section_frame(parent, "3. Selection Widgets - Complete Features")
        
        selection_frame = tk.Frame(frame, bg="white")
        selection_frame.pack(fill="both")
        
        # Left side
        left_frame = tk.Frame(selection_frame, bg="white")
        left_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        # Checkbuttons with images/indicators
        tk.Label(left_frame, text="Checkbuttons:", font=("Arial", 11, "bold"), bg="white").pack(anchor="w")
        
        self.check_var1 = tk.IntVar()
        self.check_var2 = tk.IntVar()
        self.check_var3 = tk.IntVar()
        
        tk.Checkbutton(left_frame, text="Python", variable=self.check_var1, bg="white",
                      selectcolor="#3498db", command=self.check_selection).pack(anchor="w")
        tk.Checkbutton(left_frame, text="Java", variable=self.check_var2, bg="white",
                      selectcolor="#3498db", command=self.check_selection).pack(anchor="w")
        tk.Checkbutton(left_frame, text="JavaScript", variable=self.check_var3, bg="white",
                      selectcolor="#3498db", command=self.check_selection).pack(anchor="w")
        
        self.check_result = tk.Label(left_frame, text="Selected: None", bg="white", fg="#e74c3c")
        self.check_result.pack(anchor="w", pady=5)
        
        # Radiobuttons
        tk.Label(left_frame, text="Radiobuttons:", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(10,0))
        
        self.radio_var = tk.StringVar(value="beginner")
        
        tk.Radiobutton(left_frame, text="Beginner", variable=self.radio_var, value="beginner", 
                      bg="white", selectcolor="#2ecc71", command=self.radio_selection).pack(anchor="w")
        tk.Radiobutton(left_frame, text="Intermediate", variable=self.radio_var, value="intermediate",
                      bg="white", selectcolor="#f39c12", command=self.radio_selection).pack(anchor="w")
        tk.Radiobutton(left_frame, text="Advanced", variable=self.radio_var, value="advanced",
                      bg="white", selectcolor="#e74c3c", command=self.radio_selection).pack(anchor="w")
        
        self.radio_result = tk.Label(left_frame, text="Level: Beginner", bg="white", fg="#2ecc71")
        self.radio_result.pack(anchor="w", pady=5)
        
        # Right side: Listbox with multiple selection
        right_frame = tk.Frame(selection_frame, bg="white")
        right_frame.pack(side="right", fill="both", expand=True, padx=10)
        
        tk.Label(right_frame, text="Listbox (Multiple Selection):", font=("Arial", 11, "bold"), bg="white").pack(anchor="w")
        
        listbox_frame = tk.Frame(right_frame, bg="white")
        listbox_frame.pack(fill="both", expand=True, pady=5)
        
        listbox_scroll = tk.Scrollbar(listbox_frame)
        listbox_scroll.pack(side="right", fill="y")
        
        self.listbox = tk.Listbox(listbox_frame, height=10, yscrollcommand=listbox_scroll.set,
                                 selectmode="multiple", font=("Arial", 10))
        items = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape", 
                "Honeydew", "Kiwi", "Lemon", "Mango", "Orange", "Papaya"]
        for item in items:
            self.listbox.insert("end", item)
        self.listbox.pack(side="left", fill="both", expand=True)
        listbox_scroll.config(command=self.listbox.yview)
        
        tk.Button(right_frame, text="Get Selected Items", command=self.get_listbox_selection,
                 bg="#9b59b6", fg="white").pack(pady=5)
    
    def create_display_widgets_section(self, parent):
        """Section 4: Display widgets with advanced features"""
        frame = self.create_section_frame(parent, "4. Display & Control Widgets - Advanced")
        
        # Scale widgets - horizontal and vertical
        scale_frame = tk.Frame(frame, bg="white")
        scale_frame.pack(fill="x", pady=5)
        
        left_scale = tk.Frame(scale_frame, bg="white")
        left_scale.pack(side="left", fill="both", expand=True)
        
        tk.Label(left_scale, text="Horizontal Scale:", font=("Arial", 11, "bold"), bg="white").pack(anchor="w")
        
        self.scale_var = tk.DoubleVar()
        scale1 = tk.Scale(left_scale, from_=0, to=100, orient="horizontal", 
                         variable=self.scale_var, length=300, bg="white",
                         tickinterval=20, resolution=5, showvalue=True,
                         troughcolor="#3498db", sliderlength=30)
        scale1.set(50)
        scale1.pack(anchor="w", pady=5)
        
        self.scale_label = tk.Label(left_scale, text="Value: 50", bg="white", font=("Arial", 10, "bold"))
        self.scale_label.pack(anchor="w")
        scale1.config(command=lambda v: self.scale_label.config(text=f"Value: {int(float(v))}"))
        
        right_scale = tk.Frame(scale_frame, bg="white")
        right_scale.pack(side="right", fill="both")
        
        tk.Label(right_scale, text="Vertical Scale:", font=("Arial", 11, "bold"), bg="white").pack()
        
        scale2 = tk.Scale(right_scale, from_=100, to=0, orient="vertical",
                         length=150, bg="white", troughcolor="#e74c3c")
        scale2.set(75)
        scale2.pack()
        
        # Spinbox with validation
        tk.Label(frame, text="Spinbox (with range):", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(10,0))
        
        spinbox_frame = tk.Frame(frame, bg="white")
        spinbox_frame.pack(fill="x", pady=5)
        
        spinbox = tk.Spinbox(spinbox_frame, from_=0, to=100, width=20, font=("Arial", 10),
                            increment=5, wrap=True)
        spinbox.pack(side="left", padx=5)
        
        # String spinbox
        spinbox2 = tk.Spinbox(spinbox_frame, values=("Small", "Medium", "Large", "X-Large"),
                             width=20, font=("Arial", 10), state="readonly")
        spinbox2.pack(side="left", padx=5)
        
        # Progressbar
        tk.Label(frame, text="Progressbar:", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(10,0))
        
        self.progressbar = ttk.Progressbar(frame, length=400, mode='determinate')
        self.progressbar['value'] = 0
        self.progressbar.pack(anchor="w", pady=5)
        
        progress_btn_frame = tk.Frame(frame, bg="white")
        progress_btn_frame.pack(fill="x", pady=5)
        
        tk.Button(progress_btn_frame, text="Start Progress", command=self.animate_progress,
                 bg="#2ecc71", fg="white").pack(side="left", padx=5)
        tk.Button(progress_btn_frame, text="Reset", command=lambda: self.progressbar.config(value=0),
                 bg="#e74c3c", fg="white").pack(side="left", padx=5)
    
    def create_container_widgets_section(self, parent):
        """Section 5: Container widgets"""
        frame = self.create_section_frame(parent, "5. Container Widgets (Frame, LabelFrame, PanedWindow)")
        
        # Multiple frames with different relief styles
        tk.Label(frame, text="Frames with Different Relief Styles:", font=("Arial", 11, "bold"), bg="white").pack(anchor="w")
        
        relief_frame = tk.Frame(frame, bg="white")
        relief_frame.pack(fill="x", pady=10)
        
        reliefs = ["flat", "raised", "sunken", "groove", "ridge"]
        colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"]
        
        for i, (relief, color) in enumerate(zip(reliefs, colors)):
            f = tk.Frame(relief_frame, bg=color, relief=relief, bd=5, width=150, height=80)
            f.pack(side="left", padx=5)
            f.pack_propagate(False)
            tk.Label(f, text=relief.upper(), bg=color, fg="white", font=("Arial", 10, "bold")).pack(expand=True)
        
        # LabelFrame
        tk.Label(frame, text="LabelFrame:", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(10,0))
        
        labelframe = tk.LabelFrame(frame, text="User Information", bg="white", 
                                  font=("Arial", 10, "bold"), relief="groove", bd=3,
                                  labelanchor="n")
        labelframe.pack(fill="x", pady=5)
        
        tk.Label(labelframe, text="Name:", bg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        tk.Entry(labelframe, width=30).grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(labelframe, text="Email:", bg="white").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        tk.Entry(labelframe, width=30).grid(row=1, column=1, padx=10, pady=5)
        
        # PanedWindow
        tk.Label(frame, text="PanedWindow (Drag to resize):", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(10,0))
        
        paned = tk.PanedWindow(frame, orient="horizontal", bg="white", sashwidth=5, sashrelief="raised")
        paned.pack(fill="both", expand=True, pady=5)
        
        left_pane = tk.Text(paned, width=30, height=8, bg="#ecf0f1")
        left_pane.insert("1.0", "Left pane\nResize me!")
        paned.add(left_pane)
        
        right_pane = tk.Text(paned, width=30, height=8, bg="#bdc3c7")
        right_pane.insert("1.0", "Right pane\nDrag the divider!")
        paned.add(right_pane)
    
    def create_advanced_widgets_section(self, parent):
        """Section 6: Advanced widgets"""
        frame = self.create_section_frame(parent, "6. Advanced Widgets (Canvas, Menu, Toplevel)")
        
        
        # Menubutton
        tk.Label(frame, text="Menubutton:", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(10,0))
        
        menubutton = tk.Menubutton(frame, text="File Operations ▼", relief="raised", 
                                  bg="#95a5a6", fg="white", font=("Arial", 10, "bold"),
                                  activebackground="#7f8c8d", bd=3)
        menubutton.pack(anchor="w", pady=5)
        
        menu = tk.Menu(menubutton, tearoff=0)
        menu.add_command(label="📄 New File", command=lambda: self.show_info("New File"))
        menu.add_command(label="📂 Open File", command=self.open_file)
        menu.add_command(label="💾 Save File", command=lambda: self.show_info("Save File"))
        menu.add_separator()
        menu.add_command(label="❌ Close", command=lambda: self.show_info("Close"))
        menubutton["menu"] = menu
        
        # Toplevel button
        tk.Button(frame, text="Open New Window (Toplevel)", 
                 command=self.open_toplevel, bg="#9b59b6", fg="white",
                 font=("Arial", 10, "bold"), relief="raised", bd=3).pack(anchor="w", pady=10)
    
    def create_messagebox_section(self, parent):
        """Section 7: All message box types"""
        frame = self.create_section_frame(parent, "7. Message Box Functions - All Types")
        
        tk.Label(frame, text="Information & Warning Messages:", 
                font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=5)
        
        button_frame1 = tk.Frame(frame, bg="white")
        button_frame1.pack(fill="x", pady=5)
        
        tk.Button(button_frame1, text="Show Info", command=self.show_info_demo,
                 bg="#3498db", fg="white", width=18).pack(side="left", padx=5, pady=5)
        
        tk.Button(button_frame1, text="Show Warning", command=self.show_warning_demo,
                 bg="#f39c12", fg="white", width=18).pack(side="left", padx=5, pady=5)
        
        tk.Button(button_frame1, text="Show Error", command=self.show_error_demo,
                 bg="#e74c3c", fg="white", width=18).pack(side="left", padx=5, pady=5)
        
        tk.Label(frame, text="Question Dialogs:", 
                font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(10,5))
        
        button_frame2 = tk.Frame(frame, bg="white")
        button_frame2.pack(fill="x", pady=5)
        
        tk.Button(button_frame2, text="Ask Yes/No", command=self.ask_yesno,
                 bg="#9b59b6", fg="white", width=18).pack(side="left", padx=5, pady=5)
        
        tk.Button(button_frame2, text="Ask OK/Cancel", command=self.ask_okcancel,
                 bg="#1abc9c", fg="white", width=18).pack(side="left", padx=5, pady=5)
        
        tk.Button(button_frame2, text="Ask Retry/Cancel", command=self.ask_retrycancel,
                 bg="#34495e", fg="white", width=18).pack(side="left", padx=5, pady=5)
        
        tk.Button(button_frame2, text="Ask Yes/No/Cancel", command=self.ask_yesnocancel,
                 bg="#16a085", fg="white", width=18).pack(side="left", padx=5, pady=5)
    
    def create_dialog_section(self, parent):
        """Section 8: File dialogs and other dialogs"""
        frame = self.create_section_frame(parent, "8. Dialog Boxes (File, Color, Input)")
        
        tk.Label(frame, text="File Dialogs:", font=("Arial", 11, "bold"), bg="white").pack(anchor="w")
        
        file_btn_frame = tk.Frame(frame, bg="white")
        file_btn_frame.pack(fill="x", pady=5)
        
        tk.Button(file_btn_frame, text="Open File", command=self.open_file,
                 bg="#3498db", fg="white", width=18).pack(side="left", padx=5, pady=5)
        
        tk.Button(file_btn_frame, text="Save File", command=self.save_file,
                 bg="#2ecc71", fg="white", width=18).pack(side="left", padx=5, pady=5)
        
        tk.Button(file_btn_frame, text="Select Directory", command=self.select_directory,
                 bg="#9b59b6", fg="white", width=18).pack(side="left", padx=5, pady=5)
        
        tk.Label(frame, text="Other Dialogs:", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=(10,0))
        
        other_btn_frame = tk.Frame(frame, bg="white")
        other_btn_frame.pack(fill="x", pady=5)
        
        tk.Button(other_btn_frame, text="Color Chooser", command=self.choose_color,
                 bg="#e74c3c", fg="white", width=18).pack(side="left", padx=5, pady=5)
        
        tk.Button(other_btn_frame, text="Input Dialog (String)", command=self.input_string,
                 bg="#f39c12", fg="white", width=18).pack(side="left", padx=5, pady=5)
        
        tk.Button(other_btn_frame, text="Input Dialog (Integer)", command=self.input_integer,
                 bg="#1abc9c", fg="white", width=18).pack(side="left", padx=5, pady=5)
    
    def create_event_binding_section(self, parent):
        """Section 9: Event binding examples"""
        frame = self.create_section_frame(parent, "9. Event Binding & Mouse/Keyboard Events")
        
        tk.Label(frame, text="Interactive Event Examples:", font=("Arial", 11, "bold"), bg="white").pack(anchor="w")
        
        # Click event demo
        self.click_label = tk.Label(frame, text="Click Me!", bg="#3498db", fg="white",
                                   font=("Arial", 12, "bold"), relief="raised", bd=3,
                                   width=20, height=2, cursor="hand2")
        self.click_label.pack(pady=10)
        self.click_label.bind("<Button-1>", self.on_click)
        self.click_label.bind("<Double-Button-1>", self.on_double_click)
        self.click_label.bind("<Enter>", self.on_enter)
        self.click_label.bind("<Leave>", self.on_leave)
        
        # Key binding demo
        tk.Label(frame, text="Type in this Entry (Key events will be captured):", 
                bg="white", font=("Arial", 10)).pack(anchor="w", pady=(10,0))
        
        self.key_entry = tk.Entry(frame, width=50, font=("Arial", 11))
        self.key_entry.pack(pady=5)
        self.key_entry.bind("<KeyPress>", self.on_key_press)
        self.key_entry.bind("<Return>", self.on_enter_key)
        
        self.key_info = tk.Label(frame, text="Type something...", bg="white", fg="#7f8c8d")
        self.key_info.pack(anchor="w")
        
        # Mouse motion demo
        tk.Label(frame, text="Move mouse over this canvas:", bg="white", font=("Arial", 10)).pack(anchor="w", pady=(10,0))
        
        self.motion_canvas = tk.Canvas(frame, width=500, height=100, bg="#ecf0f1", relief="sunken", bd=2)
        self.motion_canvas.pack(pady=5)
        self.motion_canvas.bind("<Motion>", self.on_mouse_motion)
        
        self.motion_text = self.motion_canvas.create_text(250, 50, text="Move mouse here", 
                                                         font=("Arial", 12), fill="#7f8c8d")
    
    def create_cursor_section(self, parent):
        """Section 10: Different cursor types"""
        frame = self.create_section_frame(parent, "10. Cursor Types")
        
        tk.Label(frame, text="Hover over buttons to see different cursors:", 
                font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=5)
        
        cursor_frame = tk.Frame(frame, bg="white")
        cursor_frame.pack(fill="x", pady=5)
        
        cursors = [
            ("arrow", "#3498db"), ("hand2", "#e74c3c"), ("cross", "#2ecc71"),
            ("watch", "#f39c12"), ("question_arrow", "#9b59b6"), ("sizing", "#1abc9c"),
            ("spider", "#e67e22"), ("target", "#34495e")
        ]
        
        for i, (cursor, color) in enumerate(cursors):
            btn = tk.Button(cursor_frame, text=cursor, cursor=cursor, bg=color, 
                          fg="white", width=15, height=2)
            btn.grid(row=i//4, column=i%4, padx=5, pady=5)
    
    def create_relief_styles_section(self, parent):
        """Section 11: All relief styles comparison"""
        frame = self.create_section_frame(parent, "11. Relief Styles Comparison")
        
        tk.Label(frame, text="All Relief Styles (flat, raised, sunken, groove, ridge, solid):", 
                font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=5)
        
        relief_frame = tk.Frame(frame, bg="white")
        relief_frame.pack(fill="x", pady=10)
        
        reliefs = ["flat", "raised", "sunken", "groove", "ridge", "solid"]
        
        for i, relief in enumerate(reliefs):
            container = tk.Frame(relief_frame, bg="white")
            container.pack(side="left", padx=10)
            
            lbl = tk.Label(container, text=relief.upper(), bg="#95a5a6", fg="white",
                          relief=relief, bd=5, width=12, height=3, font=("Arial", 10, "bold"))
            lbl.pack()
            
            tk.Label(container, text=relief, bg="white", font=("Arial", 9)).pack(pady=5)
    
    def create_anchor_section(self, parent):
        """Section 12: Anchor positions"""
        frame = self.create_section_frame(parent, "12. Anchor Positions (n, ne, e, se, s, sw, w, nw, center)")
        
        tk.Label(frame, text="Labels with different anchor positions:", 
                font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=5)
        
        anchor_frame = tk.Frame(frame, bg="white")
        anchor_frame.pack(fill="both", pady=5)
        
        anchors = [
            ("n", "North"), ("ne", "NorthEast"), ("e", "East"),
            ("se", "SouthEast"), ("s", "South"), ("sw", "SouthWest"),
            ("w", "West"), ("nw", "NorthWest"), ("center", "Center")
        ]
        
        for i, (anchor, name) in enumerate(anchors):
            lbl = tk.Label(anchor_frame, text=f"{name} ({anchor})", anchor=anchor,
                          bg="#ecf0f1", relief="solid", bd=2, width=25, height=3)
            lbl.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="nsew")
    
    def create_bitmap_section(self, parent):
        """Section 13: Built-in bitmaps"""
        frame = self.create_section_frame(parent, "13. Built-in Bitmaps")
        
        tk.Label(frame, text="Tkinter Built-in Bitmaps:", 
                font=("Arial", 11, "bold"), bg="white").pack(anchor="w", pady=5)
        
        bitmap_frame = tk.Frame(frame, bg="white")
        bitmap_frame.pack(fill="x", pady=5)
        
        bitmaps = ["error", "hourglass", "info", "questhead", "question", "warning", "gray12", "gray25", "gray50", "gray75"]
        
        for i, bitmap in enumerate(bitmaps):
            container = tk.Frame(bitmap_frame, bg="white")
            container.pack(side="left", padx=10, pady=5)
            
            try:
                lbl = tk.Label(container, bitmap=bitmap, bg="#ecf0f1", relief="raised", 
                             bd=3, width=50, height=50)
                lbl.pack()
                tk.Label(container, text=bitmap, bg="white", font=("Arial", 8)).pack()
            except:
                pass
    
    def create_statusbar(self, parent):
        """Create status bar at bottom"""
        status_frame = tk.Frame(parent, bg="#34495e", relief="sunken", bd=2)
        status_frame.pack(side="bottom", fill="x", pady=(10,0))
        
        self.status_label = tk.Label(status_frame, text="Ready | " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                     bg="#34495e", fg="white", anchor="w", padx=10)
        self.status_label.pack(side="left", fill="x", expand=True)
        
        tk.Label(status_frame, text="Complete Tkinter Demo v1.0", bg="#34495e", 
                fg="#ecf0f1", anchor="e", padx=10).pack(side="right")
    
    # Event handler methods
    def check_selection(self):
        selected = []
        if self.check_var1.get(): selected.append("Python")
        if self.check_var2.get(): selected.append("Java")
        if self.check_var3.get(): selected.append("JavaScript")
        
        if selected:
            self.check_result.config(text=f"Selected: {', '.join(selected)}")
        else:
            self.check_result.config(text="Selected: None")
    
    def radio_selection(self):
        level = self.radio_var.get()
        colors = {"beginner": "#2ecc71", "intermediate": "#f39c12", "advanced": "#e74c3c"}
        self.radio_result.config(text=f"Level: {level.capitalize()}", fg=colors[level])
    
    def get_listbox_selection(self):
        selected = [self.listbox.get(i) for i in self.listbox.curselection()]
        if selected:
            messagebox.showinfo("Selected Items", f"You selected:\n" + "\n".join(selected))
        else:
            messagebox.showinfo("Selected Items", "No items selected")
    
    def animate_progress(self):
        self.progressbar['value'] = 0
        self.update_progress()
    
    def update_progress(self):
        if self.progressbar['value'] < 100:
            self.progressbar['value'] += 10
            self.root.after(200, self.update_progress)
        else:
            messagebox.showinfo("Complete", "Progress completed!")
    
    def on_click(self, event):
        self.click_label.config(text="Clicked!", bg="#2ecc71")
        self.status_label.config(text="Label clicked!")
    
    def on_double_click(self, event):
        self.click_label.config(text="Double Clicked!", bg="#e74c3c")
        self.status_label.config(text="Label double-clicked!")
    
    def on_enter(self, event):
        self.click_label.config(bg="#f39c12", text="Mouse Over!")
    
    def on_leave(self, event):
        self.click_label.config(bg="#3498db", text="Click Me!")
    
    def on_key_press(self, event):
        self.key_info.config(text=f"Key pressed: '{event.char}' (keycode: {event.keycode})")
    
    def on_enter_key(self, event):
        text = self.key_entry.get()
        messagebox.showinfo("Enter Pressed", f"You entered: {text}")
        self.key_entry.delete(0, "end")
    
    def on_mouse_motion(self, event):
        self.motion_canvas.delete("all")
        self.motion_canvas.create_text(250, 50, 
                                      text=f"Mouse Position: ({event.x}, {event.y})",
                                      font=("Arial", 12, "bold"), fill="#2c3e50")
    
    # Dialog methods
    def open_file(self):
        filename = filedialog.askopenfilename(
            title="Select a file",
            filetypes=(("Text files", "*.txt"), ("Python files", "*.py"), ("All files", "*.*"))
        )
        if filename:
            messagebox.showinfo("File Selected", f"You selected:\n{filename}")
            self.status_label.config(text=f"Opened: {filename}")
    
    def save_file(self):
        filename = filedialog.asksaveasfilename(
            title="Save file",
            defaultextension=".txt",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if filename:
            messagebox.showinfo("File Saved", f"File saved as:\n{filename}")
            self.status_label.config(text=f"Saved: {filename}")
    
    def select_directory(self):
        directory = filedialog.askdirectory(title="Select a directory")
        if directory:
            messagebox.showinfo("Directory Selected", f"You selected:\n{directory}")
            self.status_label.config(text=f"Directory: {directory}")
    
    def choose_color(self):
        color = colorchooser.askcolor(title="Choose a color")
        if color[1]:
            messagebox.showinfo("Color Selected", f"You selected:\nRGB: {color[0]}\nHex: {color[1]}")
            self.status_label.config(text=f"Color: {color[1]}", bg=color[1])
    
    def input_string(self):
        result = simpledialog.askstring("Input", "Enter your name:")
        if result:
            messagebox.showinfo("Input Received", f"Hello, {result}!")
    
    def input_integer(self):
        result = simpledialog.askinteger("Input", "Enter your age:", minvalue=0, maxvalue=120)
        if result:
            messagebox.showinfo("Input Received", f"Your age is: {result}")
    
    # Message box methods
    def show_info(self, message):
        messagebox.showinfo("Information", message)
        self.status_label.config(text=message, bg="#34495e")
    
    def show_info_demo(self):
        messagebox.showinfo("Success", "Operation completed successfully!")
    
    def show_warning_demo(self):
        messagebox.showwarning("Warning", "Operation completed but something didn't behave as expected.")
    
    def show_error_demo(self):
        messagebox.showerror("Error", "Operation hasn't completed due to an error.")
    
    def ask_yesno(self):
        result = messagebox.askyesno("Question", "Do you like Python programming?")
        messagebox.showinfo("Result", f"You clicked: {'Yes' if result else 'No'}")
    
    def ask_okcancel(self):
        result = messagebox.askokcancel("Confirm", "Are you sure you want to proceed?")
        messagebox.showinfo("Result", f"You clicked: {'OK' if result else 'Cancel'}")
    
    def ask_retrycancel(self):
        result = messagebox.askretrycancel("Retry", "Operation failed. Do you want to retry?")
        messagebox.showinfo("Result", f"You clicked: {'Retry' if result else 'Cancel'}")
    
    def ask_yesnocancel(self):
        result = messagebox.askyesnocancel("Save", "Do you want to save changes?")
        if result is None:
            msg = "Cancel"
        elif result:
            msg = "Yes"
        else:
            msg = "No"
        messagebox.showinfo("Result", f"You clicked: {msg}")
    
    def show_about(self):
        about_text = """Complete Tkinter Demo Application
Version 1.0

This application demonstrates all Tkinter widgets,
attributes, and features including:

• All 19+ Widgets
• Standard Attributes (dimensions, colors, fonts, anchors, relief styles, bitmaps, cursors)
• Geometry Management (pack, grid, place)
• Event Binding
• Dialog Boxes
• Message Boxes

Created for learning purposes."""
        messagebox.showinfo("About", about_text)
    
    def open_toplevel(self):
        """Open a comprehensive Toplevel window"""
        top = tk.Toplevel(self.root)
        top.title("Toplevel Window with Features")
        top.geometry("500x400")
        top.configure(bg="#ecf0f1")
        
        # Make it modal (optional)
        top.grab_set()
        
        tk.Label(top, text="This is a Toplevel Window!", 
                font=("Arial", 16, "bold"), bg="#2c3e50", fg="white", pady=15).pack(fill="x")
        
        content_frame = tk.Frame(top, bg="#ecf0f1", padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        tk.Label(content_frame, text="Toplevel windows are separate windows from the main application.", 
                bg="#ecf0f1", wraplength=400, justify="left").pack(pady=10)
        
        tk.Label(content_frame, text="Features:", font=("Arial", 12, "bold"), bg="#ecf0f1").pack(anchor="w", pady=(10,5))
        
        features = [
            "• Independent window with own title bar",
            "• Can be modal or non-modal",
            "• Can have own widgets and layout",
            "• Useful for dialog boxes and forms"
        ]
        
        for feature in features:
            tk.Label(content_frame, text=feature, bg="#ecf0f1", anchor="w").pack(anchor="w", pady=2)
        
        # Add some interactive elements
        tk.Label(content_frame, text="Enter something:", bg="#ecf0f1").pack(anchor="w", pady=(15,5))
        entry = tk.Entry(content_frame, width=40)
        entry.pack(anchor="w")
        
        btn_frame = tk.Frame(content_frame, bg="#ecf0f1")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Show Input", 
                 command=lambda: messagebox.showinfo("Input", f"You entered: {entry.get()}" if entry.get() else "Nothing entered"),
                 bg="#3498db", fg="white", width=15).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Close Window", command=top.destroy,
                 bg="#e74c3c", fg="white", width=15).pack(side="left", padx=5)

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = CompleteTkinterApp(root)
    root.mainloop()