import os
import platform
from tkinter import filedialog, Button, Label, StringVar, Entry, messagebox, Listbox, Scrollbar, Frame, ttk, IntVar, Checkbutton
from tkinter.font import Font
from convertor_core import convert_file, convert_folder, combine_files

class ConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown Converter Pro")
        self.root.geometry("800x650")
        self.root.resizable(True, True)
        
        # Set theme colors
        self.primary_color = "#3498db"  # Blue
        self.secondary_color = "#2980b9"  # Darker blue
        self.bg_color = "#f5f5f5"  # Light gray
        self.text_color = "#2c3e50"  # Dark blue/gray
        self.success_color = "#2ecc71"  # Green
        self.warning_color = "#e74c3c"  # Red
        
        # Set system-appropriate fonts
        if platform.system() == "Darwin":  # macOS
            self.header_font = Font(family="SF Pro Display", size=14, weight="bold")
            self.normal_font = Font(family="SF Pro Text", size=12)
            self.small_font = Font(family="SF Pro Text", size=10)
        elif platform.system() == "Windows":
            self.header_font = Font(family="Segoe UI", size=12, weight="bold")
            self.normal_font = Font(family="Segoe UI", size=10)
            self.small_font = Font(family="Segoe UI", size=9)
        else:  # Linux and others
            self.header_font = Font(family="Ubuntu", size=12, weight="bold")
            self.normal_font = Font(family="Ubuntu", size=10)
            self.small_font = Font(family="Ubuntu", size=9)
        
        # Configure root window appearance
        self.root.configure(bg=self.bg_color)
        
        # Configure ttk styles
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use clam theme as base
        
        # Configure notebook style
        self.style.configure("TNotebook", background=self.bg_color, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=self.bg_color, foreground=self.text_color,
                            padding=[10, 5], font=self.normal_font)
        self.style.map("TNotebook.Tab", background=[("selected", self.primary_color)],
                      foreground=[("selected", "white")])
        
        # Configure frame style
        self.style.configure("TFrame", background=self.bg_color)
        
        # Configure button style
        self.style.configure("TButton", background=self.primary_color, foreground="white", 
                           font=self.normal_font, padding=5)
        self.style.map("TButton", background=[("active", self.secondary_color)])
        
        # Configure combobox style
        self.style.configure("TCombobox", background="white", foreground=self.text_color, 
                           fieldbackground="white", font=self.normal_font)
        
        # File list
        self.files = []
        
        # Create app title
        title_frame = Frame(root, bg=self.bg_color)
        title_frame.pack(fill="x", padx=20, pady=10)
        
        app_title = Label(title_frame, text="Markdown Converter Pro", font=Font(family=self.header_font.cget("family"), 
                                                                           size=18, weight="bold"),
                       fg=self.primary_color, bg=self.bg_color)
        app_title.pack(side="left")
        
        app_subtitle = Label(title_frame, text="Convert & Combine Markdown Files", 
                           font=self.normal_font, fg=self.text_color, bg=self.bg_color)
        app_subtitle.pack(side="left", padx=10)
        
        # Create tabs
        self.tab_control = ttk.Notebook(root)
        
        # Single file/folder tab
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text='Single File/Folder')
        
        # Multiple files tab
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab2, text='Multiple Files')
        
        self.tab_control.pack(expand=1, fill="both", padx=20, pady=10)
        
        # Output format selection
        self.output_formats = ['docx', 'pdf', 'html', 'odt', 'rtf', 'tex', 'epub']
        self.format_var = StringVar()
        self.format_var.set('docx')
        
        # Configure the single file/folder tab
        self.setup_single_tab()
        
        # Configure the multiple files tab
        self.setup_multiple_tab()
    
    def setup_single_tab(self):
        # Create section title
        section_frame = Frame(self.tab1, bg=self.bg_color)
        section_frame.grid(row=0, column=0, columnspan=4, sticky="w", padx=15, pady=(15, 5))
        
        icon_label = Label(section_frame, text="📄", font=Font(size=16), bg=self.bg_color, fg=self.primary_color)
        icon_label.pack(side="left")
        
        section_label = Label(section_frame, text="Single File/Folder Conversion", 
                           font=self.header_font, bg=self.bg_color, fg=self.text_color)
        section_label.pack(side="left", padx=5)
        
        # Input frame with shadow effect
        input_frame = Frame(self.tab1, bg="white", highlightbackground="#dddddd", 
                          highlightcolor="#dddddd", highlightthickness=1)
        input_frame.grid(row=1, column=0, columnspan=4, padx=15, pady=10, sticky="ew")
        
        # File or Folder selection
        self.path_var = StringVar()
        Label(input_frame, text="Select Markdown File or Folder:", font=self.normal_font, 
             bg="white", fg=self.text_color).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        input_entry = Entry(input_frame, textvariable=self.path_var, width=50, font=self.normal_font,
                          bd=1, relief="solid")
        input_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        
        button_frame = Frame(input_frame, bg="white")
        button_frame.grid(row=0, column=2, padx=5, pady=10)
        
        browse_file_btn = ttk.Button(button_frame, text="Browse File", command=self.browse_file, style="TButton")
        browse_file_btn.pack(side="left", padx=2)
        
        browse_folder_btn = ttk.Button(button_frame, text="Browse Folder", command=self.browse_folder, style="TButton")
        browse_folder_btn.pack(side="left", padx=2)
        
        # Output options frame
        output_frame = Frame(self.tab1, bg="white", highlightbackground="#dddddd", 
                           highlightcolor="#dddddd", highlightthickness=1)
        output_frame.grid(row=2, column=0, columnspan=4, padx=15, pady=10, sticky="ew")
        
        # Output path
        self.output_var = StringVar()
        Label(output_frame, text="Output Location (optional):", font=self.normal_font, 
             bg="white", fg=self.text_color).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        output_entry = Entry(output_frame, textvariable=self.output_var, width=50, font=self.normal_font,
                           bd=1, relief="solid")
        output_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        
        output_browse_btn = ttk.Button(output_frame, text="Browse", command=self.browse_output, style="TButton")
        output_browse_btn.grid(row=0, column=2, padx=5, pady=10)
        
        # Output format
        Label(output_frame, text="Output Format:", font=self.normal_font, 
             bg="white", fg=self.text_color).grid(row=1, column=0, sticky="w", padx=10, pady=10)
        
        # Format frame with icons
        format_frame = Frame(output_frame, bg="white")
        format_frame.grid(row=1, column=1, sticky="w", padx=5, pady=10)
        
        format_dropdown = ttk.Combobox(format_frame, textvariable=self.format_var, 
                                      values=self.output_formats, font=self.normal_font, width=15)
        format_dropdown.pack(side="left")
        
        # Format icon indicator
        self.format_icon_var = StringVar()
        self.format_icon_var.set("📄")
        self.format_var.trace_add("write", self.update_format_icon)
        
        format_icon = Label(format_frame, textvariable=self.format_icon_var, font=Font(size=16),
                          bg="white", fg=self.text_color)
        format_icon.pack(side="left", padx=10)
        
        # Action button frame
        action_frame = Frame(self.tab1, bg=self.bg_color)
        action_frame.grid(row=3, column=0, columnspan=4, pady=20, sticky="ew")
        action_frame.grid_columnconfigure(0, weight=1)
        
        # Convert button with modern styling
        convert_button = Button(action_frame, text="Convert Document", command=self.convert_single,
                              font=self.header_font, bg=self.primary_color, fg="white",
                              activebackground=self.secondary_color, activeforeground="white",
                              bd=0, padx=20, pady=10, cursor="hand2")
        convert_button.grid(row=0, column=0)
        
        # Status frame with border
        status_frame = Frame(self.tab1, bg="white", highlightbackground="#dddddd", 
                           highlightcolor="#dddddd", highlightthickness=1)
        status_frame.grid(row=4, column=0, columnspan=4, padx=15, pady=10, sticky="ew")
        
        # Status label
        self.status_var1 = StringVar()
        self.status_var1.set("Ready to convert")
        
        # Status icon
        self.status_icon1 = Label(status_frame, text="🔹", font=Font(size=16), 
                                bg="white", fg=self.primary_color)
        self.status_icon1.pack(side="left", padx=10, pady=10)
        
        # Status text
        status_label = Label(status_frame, textvariable=self.status_var1, wraplength=680,
                           font=self.normal_font, bg="white", fg=self.text_color, justify="left")
        status_label.pack(side="left", padx=5, pady=10, fill="x", expand=True)
        
        # Configure grid weights for responsive design
        self.tab1.grid_columnconfigure(1, weight=1)
    
    def browse_file(self):
        """Open file browser to select a markdown file"""
        file_path = filedialog.askopenfilename(
            title="Select Markdown File",
            filetypes=[("Markdown Files", "*.md *.markdown"), ("All Files", "*.*")]
        )
        if file_path:
            self.path_var.set(file_path)
    
    def browse_folder(self):
        """Open folder browser to select a directory with markdown files"""
        folder_path = filedialog.askdirectory(title="Select Folder with Markdown Files")
        if folder_path:
            self.path_var.set(folder_path)
    
    def browse_output(self):
        """Open file browser to select output file location"""
        output_format = self.format_var.get()
        file_path = filedialog.asksaveasfilename(
            title="Save Output As",
            defaultextension=f".{output_format}",
            filetypes=[("{}".format(output_format.upper()), f"*.{output_format}")]
        )
        if file_path:
            self.output_var.set(file_path)
    
    def update_format_icon(self, *args):
        """Update the format icon based on selected format"""
        format_icons = {
            'docx': '📄', 'pdf': '📑', 'html': '🌐', 
            'odt': '📝', 'rtf': '📄', 'tex': '📚', 'epub': '📱'
        }
        selected_format = self.format_var.get()
        self.format_icon_var.set(format_icons.get(selected_format, '📄'))
    
    def convert_single(self):
        """Convert a single file or all files in a folder"""
        input_path = self.path_var.get()
        output_path = self.output_var.get() if self.output_var.get() else None
        output_format = self.format_var.get()
        
        if not input_path:
            messagebox.showerror("Error", "Please select an input file or folder")
            return
        
        # Update status
        self.status_var1.set("Converting...")
        self.status_icon1.config(text="⏳", fg="#f39c12")
        self.root.update_idletasks()
        
        try:
            if os.path.isdir(input_path):
                # Process directory
                success_count, error_count, error_files = convert_folder(
                    input_path, output_path, output_format
                )
                
                if success_count > 0:
                    self.status_var1.set(
                        f"Successfully converted {success_count} files. " + 
                        (f"{error_count} errors occurred." if error_count > 0 else "")
                    )
                    self.status_icon1.config(text="✅", fg=self.success_color)
                else:
                    self.status_var1.set(f"No files were converted. {error_count} errors occurred.")
                    self.status_icon1.config(text="❌", fg=self.warning_color)
            else:
                # Process single file
                success, result = convert_file(input_path, output_path, output_format)
                
                if success:
                    self.status_var1.set(f"Successfully converted to {result}")
                    self.status_icon1.config(text="✅", fg=self.success_color)
                else:
                    self.status_var1.set(f"Error: {result}")
                    self.status_icon1.config(text="❌", fg=self.warning_color)
        except Exception as e:
            self.status_var1.set(f"Error: {str(e)}")
            self.status_icon1.config(text="❌", fg=self.warning_color)
    
    def setup_multiple_tab(self):
        # Create section title
        section_frame = Frame(self.tab2, bg=self.bg_color)
        section_frame.grid(row=0, column=0, columnspan=4, sticky="w", padx=15, pady=(15, 5))
        
        icon_label = Label(section_frame, text="📚", font=Font(size=16), bg=self.bg_color, fg=self.primary_color)
        icon_label.pack(side="left")
        
        section_label = Label(section_frame, text="Multiple Files Combination", 
                           font=self.header_font, bg=self.bg_color, fg=self.text_color)
        section_label.pack(side="left", padx=5)
        
        # File list frame with shadow effect
        file_frame = Frame(self.tab2, bg="white", highlightbackground="#dddddd", 
                         highlightcolor="#dddddd", highlightthickness=1)
        file_frame.grid(row=1, column=0, columnspan=4, padx=15, pady=10, sticky="nsew")
        
        # File list header with icon
        file_header_frame = Frame(file_frame, bg="white")
        file_header_frame.pack(fill="x", padx=10, pady=10)
        
        file_icon = Label(file_header_frame, text="📋", font=Font(size=14), bg="white", fg=self.primary_color)
        file_icon.pack(side="left")
        
        file_label = Label(file_header_frame, text="Selected Files:", font=self.normal_font, 
                         bg="white", fg=self.text_color)
        file_label.pack(side="left", padx=5)
        
        # File counter
        self.file_count_var = StringVar()
        self.file_count_var.set("(0 files)")
        file_count = Label(file_header_frame, textvariable=self.file_count_var, 
                         font=self.small_font, bg="white", fg=self.text_color)
        file_count.pack(side="left", padx=5)
        
        # File list with scrollbar in a nice container
        list_container = Frame(file_frame, bg="white", bd=1, relief="solid")
        list_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Scrollbar styling
        scrollbar = Scrollbar(list_container)
        scrollbar.pack(side="right", fill="y")
        
        # Listbox with custom colors
        self.file_listbox = Listbox(list_container, width=80, height=12, font=self.normal_font,
                                  bg="white", fg=self.text_color, bd=0, highlightthickness=0,
                                  selectbackground=self.primary_color, selectforeground="white")
        self.file_listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar.config(command=self.file_listbox.yview)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        
        # Buttons for file management in a nice toolbar
        button_frame = Frame(file_frame, bg="white")
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        add_btn = ttk.Button(button_frame, text="➕ Add Files", command=self.add_files, style="TButton")
        add_btn.pack(side="left", padx=2)
        
        remove_btn = ttk.Button(button_frame, text="➖ Remove Selected", command=self.remove_file, style="TButton")
        remove_btn.pack(side="left", padx=2)
        
        clear_btn = ttk.Button(button_frame, text="🗑️ Clear All", command=self.clear_files, style="TButton")
        clear_btn.pack(side="left", padx=2)
        
        # Output options frame
        options_frame = Frame(self.tab2, bg="white", highlightbackground="#dddddd", 
                            highlightcolor="#dddddd", highlightthickness=1)
        options_frame.grid(row=2, column=0, columnspan=4, padx=15, pady=10, sticky="ew")
        
        # Options header
        options_header = Frame(options_frame, bg="white")
        options_header.pack(fill="x", padx=10, pady=10)
        
        options_icon = Label(options_header, text="⚙️", font=Font(size=14), bg="white", fg=self.primary_color)
        options_icon.pack(side="left")
        
        options_label = Label(options_header, text="Output Options", font=self.normal_font, 
                           bg="white", fg=self.text_color)
        options_label.pack(side="left", padx=5)
        
        # Checkbox for combining files
        checkbox_frame = Frame(options_frame, bg="white")
        checkbox_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        self.combine_var = IntVar()
        self.combine_var.set(1)
        
        # Custom checkbox style
        combine_check = Checkbutton(checkbox_frame, text="Combine all files into a single document", 
                                  variable=self.combine_var, font=self.normal_font,
                                  bg="white", fg=self.text_color, 
                                  activebackground="white", activeforeground=self.primary_color,
                                  selectcolor="white")
        combine_check.pack(anchor="w")
        
        # Output file options
        output_container = Frame(options_frame, bg="white")
        output_container.pack(fill="x", padx=20, pady=(0, 10))
        
        # Output file path
        output_path_frame = Frame(output_container, bg="white")
        output_path_frame.pack(fill="x", pady=5)
        
        Label(output_path_frame, text="Output File:", font=self.normal_font, 
             bg="white", fg=self.text_color, width=15, anchor="w").pack(side="left")
        
        self.output_var2 = StringVar()
        output_entry = Entry(output_path_frame, textvariable=self.output_var2, 
                          font=self.normal_font, bd=1, relief="solid", width=40)
        output_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        output_browse_btn = ttk.Button(output_path_frame, text="Browse", 
                                     command=self.browse_output_combined, style="TButton")
        output_browse_btn.pack(side="left", padx=5)
        
        # Output format with icons
        format_frame = Frame(output_container, bg="white")
        format_frame.pack(fill="x", pady=5)
        
        Label(format_frame, text="Output Format:", font=self.normal_font, 
             bg="white", fg=self.text_color, width=15, anchor="w").pack(side="left")
        
        format_select_frame = Frame(format_frame, bg="white")
        format_select_frame.pack(side="left")
        
        self.format_var2 = StringVar()
        self.format_var2.set('docx')
        
        format_dropdown2 = ttk.Combobox(format_select_frame, textvariable=self.format_var2, 
                                      values=self.output_formats, font=self.normal_font, width=15)
        format_dropdown2.pack(side="left")
        
        # Format icon indicator for tab 2
        self.format_icon_var2 = StringVar()
        self.format_icon_var2.set("📄")
        self.format_var2.trace_add("write", self.update_format_icon2)
        
        format_icon2 = Label(format_select_frame, textvariable=self.format_icon_var2, 
                          font=Font(size=16), bg="white", fg=self.text_color)
        format_icon2.pack(side="left", padx=10)
        
        # Action button frame
        action_frame = Frame(self.tab2, bg=self.bg_color)
        action_frame.grid(row=3, column=0, columnspan=4, pady=20, sticky="ew")
        action_frame.grid_columnconfigure(0, weight=1)
        
        # Convert button with modern styling
        convert_button = Button(action_frame, text="Combine & Convert Documents", command=self.convert_multiple,
                              font=self.header_font, bg=self.primary_color, fg="white",
                              activebackground=self.secondary_color, activeforeground="white",
                              bd=0, padx=20, pady=10, cursor="hand2")
        convert_button.grid(row=0, column=0)
        
        # Status frame with border
        status_frame = Frame(self.tab2, bg="white", highlightbackground="#dddddd", 
                           highlightcolor="#dddddd", highlightthickness=1)
        status_frame.grid(row=4, column=0, columnspan=4, padx=15, pady=10, sticky="ew")
        
        # Status label
        self.status_var2 = StringVar()
        self.status_var2.set("Ready to convert")
        
        # Status icon
        self.status_icon2 = Label(status_frame, text="🔹", font=Font(size=16), 
                                bg="white", fg=self.primary_color)
        self.status_icon2.pack(side="left", padx=10, pady=10)
        
        # Status text
        status_label = Label(status_frame, textvariable=self.status_var2, wraplength=680,
                           font=self.normal_font, bg="white", fg=self.text_color, justify="left")
        status_label.pack(side="left", padx=5, pady=10, fill="x", expand=True)
        
        # Configure grid weights to make the listbox expandable
        self.tab2.grid_rowconfigure(1, weight=1)
        self.tab2.grid_columnconfigure(0, weight=1)
    
    def add_files(self):
        """Open file browser to select multiple markdown files"""
        file_paths = filedialog.askopenfilenames(
            title="Select Markdown Files",
            filetypes=[("Markdown Files", "*.md *.markdown"), ("All Files", "*.*")]
        )
        if file_paths:
            for file_path in file_paths:
                if file_path not in self.files:
                    self.files.append(file_path)
                    self.file_listbox.insert("end", os.path.basename(file_path))
            
            # Update file count
            self.file_count_var.set(f"({len(self.files)} files)")
    
    def remove_file(self):
        """Remove selected file from the list"""
        try:
            selected_index = self.file_listbox.curselection()[0]
            self.file_listbox.delete(selected_index)
            self.files.pop(selected_index)
            
            # Update file count
            self.file_count_var.set(f"({len(self.files)} files)")
        except (IndexError, TypeError):
            messagebox.showinfo("Info", "Please select a file to remove")
    
    def clear_files(self):
        """Clear all files from the list"""
        self.file_listbox.delete(0, "end")
        self.files = []
        self.file_count_var.set("(0 files)")
    
    def browse_output_combined(self):
        """Open file browser to select combined output file location"""
        output_format = self.format_var2.get()
        file_path = filedialog.asksaveasfilename(
            title="Save Combined Output As",
            defaultextension=f".{output_format}",
            filetypes=[("{}".format(output_format.upper()), f"*.{output_format}")]
        )
        if file_path:
            self.output_var2.set(file_path)
    
    def update_format_icon2(self, *args):
        """Update the format icon based on selected format for tab 2"""
        format_icons = {
            'docx': '📄', 'pdf': '📑', 'html': '🌐', 
            'odt': '📝', 'rtf': '📄', 'tex': '📚', 'epub': '📱'
        }
        selected_format = self.format_var2.get()
        self.format_icon_var2.set(format_icons.get(selected_format, '📄'))
    
    def convert_multiple(self):
        """Convert multiple files, optionally combining them"""
        if not self.files:
            messagebox.showerror("Error", "Please add files to convert")
            return
        
        output_path = self.output_var2.get()
        output_format = self.format_var2.get()
        
        # For combined mode, ensure output path is provided
        if self.combine_var.get() == 1 and not output_path:
            messagebox.showerror("Error", "Please specify an output file")
            return
        
        # Update status
        self.status_var2.set("Processing...")
        self.status_icon2.config(text="⏳", fg="#f39c12")
        self.root.update_idletasks()
        
        try:
            if self.combine_var.get() == 1:
                # Combine files
                success, result = combine_files(self.files, output_path, output_format)
                
                if success:
                    self.status_var2.set(f"Successfully combined {len(self.files)} files into {result}")
                    self.status_icon2.config(text="✅", fg=self.success_color)
                else:
                    self.status_var2.set(f"Error: {result}")
                    self.status_icon2.config(text="❌", fg=self.warning_color)
            else:
                # Convert each file individually
                success_count = 0
                error_count = 0
                error_files = []
                
                for file_path in self.files:
                    # Generate output path if not specified
                    file_output = None
                    if output_path:
                        # If output is a directory, use it for output
                        if os.path.isdir(output_path):
                            file_output = os.path.join(
                                output_path, 
                                os.path.splitext(os.path.basename(file_path))[0] + f".{output_format}"
                            )
                    
                    success, result = convert_file(file_path, file_output, output_format)
                    
                    if success:
                        success_count += 1
                    else:
                        error_count += 1
                        error_files.append((os.path.basename(file_path), result))
                
                if success_count > 0:
                    self.status_var2.set(
                        f"Successfully converted {success_count} files. " + 
                        (f"{error_count} errors occurred." if error_count > 0 else "")
                    )
                    self.status_icon2.config(text="✅", fg=self.success_color)
                else:
                    self.status_var2.set(f"No files were converted. {error_count} errors occurred.")
                    self.status_icon2.config(text="❌", fg=self.warning_color)
        except Exception as e:
            self.status_var2.set(f"Error: {str(e)}")
            self.status_icon2.config(text="❌", fg=self.warning_color)