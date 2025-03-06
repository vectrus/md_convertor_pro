import os
import sys
import platform
from tkinter import Tk, Button, messagebox
from convertor_gui import ConverterGUI
from convertor_core import convert_file, convert_folder, combine_files, preprocess_markdown_lists

def show_splash_screen():
    """Show a splash screen while loading"""
    from tkinter import Label, Frame
    from tkinter.font import Font
    
    splash = Tk()
    splash.overrideredirect(True)  # Remove window decorations
    
    # Get screen width and height
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    
    # Set splash window size and position
    width = 400
    height = 300
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    splash.geometry(f"{width}x{height}+{x}+{y}")
    
    # Configure splash window
    splash.configure(bg="#3498db")
    
    # Add logo/icon
    logo_frame = Frame(splash, bg="#3498db")
    logo_frame.pack(pady=20)
    
    logo_text = Label(logo_frame, text="📚", font=("Arial", 48), bg="#3498db", fg="white")
    logo_text.pack()
    
    # Add app name
    title = Label(splash, text="Markdown Converter Pro", font=("Arial", 20, "bold"), 
                bg="#3498db", fg="white")
    title.pack(pady=10)
    
    # Add loading text
    loading_text = Label(splash, text="Loading...", font=("Arial", 12), 
                       bg="#3498db", fg="white")
    loading_text.pack(pady=20)
    
    # Add loading bar
    progress_frame = Frame(splash, bg="#3498db")
    progress_frame.pack(pady=10, padx=50, fill="x")
    
    progress_bg = Frame(progress_frame, bg="white", height=20)
    progress_bg.pack(fill="x")
    
    progress_bar = Frame(progress_bg, bg="#2ecc71", width=0, height=20)
    progress_bar.place(x=0, y=0)
    
    # Add version info
    version_label = Label(splash, text="Version 1.0.0", font=("Arial", 8), 
                        bg="#3498db", fg="white")
    version_label.pack(side="bottom", pady=10)
    
    # Animate the progress bar
    def update_progress_bar(value):
        width = int(394 * (value / 100))  # 394 is full width minus padding
        progress_bar.config(width=width)
        splash.update_idletasks()
        
    # Simulate loading
    for i in range(101):
        splash.after(20, update_progress_bar(i))
        splash.update()
        
    splash.after(500)  # Show completed progress for a moment
    splash.destroy()
    
    return

def main():
    if len(sys.argv) > 1:
        # Command line mode
        if sys.argv[1] == "--combine" and len(sys.argv) > 3:
            # Combine multiple files
            input_files = sys.argv[2:-1]  # All arguments except the last one (output file)
            output_path = sys.argv[-1]
            output_format = os.path.splitext(output_path)[1][1:]  # Get extension without dot
            
            print(f"Combining {len(input_files)} files into {output_path}")
            success, result = combine_files(input_files, output_path, output_format)
            
            if success:
                print(f"Successfully combined files into {result}")
            else:
                print(f"Error: {result}")
        elif os.path.isdir(sys.argv[1]):
            # Convert all markdown files in the folder
            output_folder = sys.argv[2] if len(sys.argv) > 2 else None
            output_format = sys.argv[3] if len(sys.argv) > 3 else 'docx'
            
            success_count, error_count, error_files = convert_folder(sys.argv[1], output_folder, output_format)
            
            print(f"Converted {success_count} files to {output_format.upper()} format")
            if error_count > 0:
                print(f"Encountered {error_count} errors:")
                for name, err in error_files:
                    print(f"- {name}: {err}")
        else:
            # Convert a single file
            output_path = sys.argv[2] if len(sys.argv) > 2 else None
            output_format = os.path.splitext(output_path)[1][1:] if output_path else 'docx'
            
            success, result = convert_file(sys.argv[1], output_path, output_format)
            
            if success:
                print(f"Successfully converted to {result}")
            else:
                print(f"Error: {result}")
    else:
        # GUI mode
        # Show splash screen
        show_splash_screen()
        
        # Create main window
        root = Tk()
        
        # Set window icon (for Windows)
        # Comment out problematic iconbitmap call
        # if platform.system() == "Windows":
        #     root.iconbitmap(default="NONE")
        
        # Set app name in taskbar
        root.title("Markdown Converter Pro")
        
        app = ConverterGUI(root)
        
        # Center window on screen
        window_width = 800
        window_height = 650
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        root.mainloop()

if __name__ == "__main__":
    main()