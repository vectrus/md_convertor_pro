import os
import pypandoc

def convert_file(input_path, output_path=None, output_format='docx'):
    """Convert a markdown file to the specified format using pandoc"""
    try:
        # If no output path is specified, create one based on the input path
        if output_path is None:
            output_path = os.path.splitext(input_path)[0] + '.' + output_format
        
        # Read and preprocess the markdown content
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ensure proper list formatting by adding blank lines before and after lists
        # and ensuring each list item is properly formatted with spaces
        content = preprocess_markdown_lists(content)
            
        # Write preprocessed content to a temporary file
        temp_filename = "temp_" + os.path.basename(input_path)
        with open(temp_filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Additional pandoc options to better handle lists
        extra_args = [
            '--wrap=preserve',      # Preserve line wrapping
            '--markdown-headings=atx',  # Use # style headings
        ]
        
        # Convert the file with the additional options
        pypandoc.convert_file(temp_filename, output_format, outputfile=output_path, extra_args=extra_args)
        
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
            
        return True, output_path
    except Exception as e:
        # Clean up in case of error
        temp_filename = "temp_" + os.path.basename(input_path)
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        return False, str(e)

def convert_folder(input_folder, output_folder=None, output_format='docx'):
    """Convert all markdown files in a folder to the specified format"""
    # If no output folder is specified, use the input folder
    if output_folder is None:
        output_folder = input_folder
    
    # Check if output folder exists, create it if it doesn't
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Initialize counters
    success_count = 0
    error_count = 0
    error_files = []
    
    # Process each markdown file in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.md', '.markdown')):
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + '.' + output_format
            output_path = os.path.join(output_folder, output_filename)
            
            success, result = convert_file(input_path, output_path, output_format)
            if success:
                success_count += 1
            else:
                error_count += 1
                error_files.append((filename, result))
    
    return success_count, error_count, error_files

def combine_files(input_files, output_path, output_format='docx'):
    """Combine multiple markdown files into a single document"""
    try:
        # Create a temporary file with all content combined
        combined_content = ""
        file_headers = []
        
        for i, file_path in enumerate(input_files):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Preprocess the content to fix list formatting
                content = preprocess_markdown_lists(content)
                
                # Add a page break between files except for the first one
                if i > 0:
                    combined_content += "\n\n\\pagebreak\n\n"
                
                # Extract filename without extension for a header
                filename = os.path.basename(file_path)
                file_base = os.path.splitext(filename)[0]
                file_headers.append(file_base)
                
                # Add a header for each file
                combined_content += f"# {file_base}\n\n"
                combined_content += content
        
        # Create a temporary file
        temp_file = "combined_temp.md"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(combined_content)
        
        # Additional pandoc options to better handle lists
        extra_args = [
            '--wrap=preserve',      # Preserve line wrapping
            '--markdown-headings=atx',  # Use # style headings
        ]
        
        # Convert the combined file with additional options
        pypandoc.convert_file(temp_file, output_format, outputfile=output_path, extra_args=extra_args)
        
        # Clean up the temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        return True, output_path
    except Exception as e:
        # Clean up in case of error
        if os.path.exists("combined_temp.md"):
            os.remove("combined_temp.md")
        return False, str(e)

def preprocess_markdown_lists(content):
    """Preprocess markdown content to ensure proper list formatting"""
    lines = content.split('\n')
    result = []
    in_list = False
    
    for i, line in enumerate(lines):
        # Check if this line is a list item
        is_list_item = line.strip().startswith(('-', '*', '+')) or (line.strip() and line.strip()[0].isdigit() and '.' in line.strip()[:3])
        
        # If entering a list
        if is_list_item and not in_list:
            in_list = True
            # Ensure there's a blank line before the list if not at the beginning
            if i > 0 and result and result[-1].strip():
                result.append('')
        
        # If exiting a list
        elif not is_list_item and in_list and line.strip():
            in_list = False
            # Ensure there's a blank line after the list
            if result and result[-1].strip():
                result.append('')
        
        # Process list items to ensure proper formatting
        if is_list_item:
            # For bullet lists, ensure proper spacing
            if line.strip().startswith(('-', '*', '+')):
                marker = line.strip()[0]
                text = line.strip()[1:].strip()
                # Ensure the list item has a space after the marker
                line = f"{marker} {text}"
            # For numbered lists, ensure proper spacing
            elif line.strip() and line.strip()[0].isdigit() and '.' in line.strip()[:3]:
                parts = line.strip().split('.', 1)
                number = parts[0]
                text = parts[1].strip()
                # Ensure the list item has a space after the marker
                line = f"{number}. {text}"
        
        result.append(line)
    
    return '\n'.join(result)