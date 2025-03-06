# 📚 Markdown Converter Pro

A modern Python application for converting and combining Markdown files into various output formats with a clean, user-friendly interface.

![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **Single File Conversion**: Transform individual Markdown files into your preferred format
- **Batch Processing**: Convert all Markdown files in a folder at once
- **File Combination**: Merge multiple Markdown files into a single document
- **Multiple Output Formats**: Export to DOCX, PDF, HTML, ODT, RTF, TEX, or EPUB
- **Smart List Formatting**: Automatic preprocessing ensures consistent list formatting
- **Modern UI**: Clean, responsive interface with visual feedback

## 🛠️ Dependencies

### Required Python Packages

| Package | Version | Purpose |
|---------|---------|---------|
| [pypandoc](https://github.com/JessicaTegner/pypandoc) | Latest | Python wrapper for Pandoc document conversion |
| [tkinter](https://docs.python.org/3/library/tkinter.html) | Built-in | GUI toolkit for the application interface |

### External Dependencies

- **[Pandoc](https://pandoc.org/)** (must be installed separately)
  - Universal document converter
  - Required for all conversion operations
  - Installation guides: [Windows](https://pandoc.org/installing.html#windows), [macOS](https://pandoc.org/installing.html#macos), [Linux](https://pandoc.org/installing.html#linux)

## 🚀 Installation

1. Clone or download this repository
2. Install Python dependencies:
   ```bash
   pip install pypandoc
   ```
3. Install Pandoc from their [official website](https://pandoc.org/installing.html)
4. Verify your installation:
   ```bash
   pandoc --version
   ```

## 🖥️ Usage

### GUI Mode

Launch the application with:

```bash
python main.py
```

Or simply run `start.bat` on Windows.

#### Single File/Folder Tab
- Select a Markdown file or folder containing Markdown files
- Choose your desired output format (DOCX, PDF, HTML, etc.)
- Optionally specify an output location
- Click "Convert Document"

#### Multiple Files Tab
- Add multiple Markdown files to the list
- Choose whether to combine them or convert individually
- Select your desired output format
- Click "Combine & Convert Documents"

### Command Line Mode

**Convert a single file:**
```bash
python main.py input.md output.docx
```

**Convert all Markdown files in a folder:**
```bash
python main.py /path/to/folder /output/folder docx
```

**Combine multiple files:**
```bash
python main.py --combine file1.md file2.md file3.md output.docx
```

## 🔧 Troubleshooting

### Common Issues

1. **"No module named 'convertor_gui'"**
   - Fixed naming inconsistency in the imports. Use the correct module names:
     - `from convertor_gui import ConverterGUI`
     - `from convertor_core import ...`

2. **Pandoc-related errors**
   - Ensure Pandoc is correctly installed and accessible in your PATH
   - Try running `pandoc --version` in your terminal to verify

3. **List formatting issues**
   - The application preprocesses Markdown lists for better compatibility
   - If you encounter formatting problems, check the original list syntax

## 🏗️ Project Structure

- `main.py` - Entry point and command-line interface
- `convertor_gui.py` - GUI implementation with tkinter
- `convertor_core.py` - Core conversion functions using pypandoc
- `start.bat` - Convenience batch file for Windows users

## 📝 License

This project is released under the MIT License.

## 🙏 Acknowledgements

- [Pandoc](https://pandoc.org/) for the powerful document conversion engine
- [pypandoc](https://github.com/JessicaTegner/pypandoc) for the Python wrapper