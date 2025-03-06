# Markdown Converter Pro

A Python application for converting and combining Markdown files into various formats using Pandoc.

## Issue Fixed

There was a naming inconsistency in the imports. The file names used "convertor" (with "or") but the imports were looking for "converter" (with "er"). This caused the following error:

```
ModuleNotFoundError: No module named 'converter_gui'
```

The fix was to update the imports in `main.py` and `convertor_gui.py` to match the actual file names:

1. In `main.py`:
   - Changed `from converter_gui import ConverterGUI` to `from convertor_gui import ConverterGUI`
   - Changed `from converter_core import ...` to `from convertor_core import ...`

2. In `convertor_gui.py`:
   - Changed `from converter_core import ...` to `from convertor_core import ...`

## Running the Application

To run the application:

```
python main.py
```

## Dependencies

This application requires:
- Python 3.x
- pypandoc
- tkinter (usually comes with Python)
- Pandoc (must be installed separately)

## Features

- Convert single Markdown files to various formats (DOCX, PDF, HTML, ODT, RTF, TEX, EPUB)
- Convert all Markdown files in a folder
- Combine multiple Markdown files into a single document
- User-friendly GUI with modern styling
