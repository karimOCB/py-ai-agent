import os

def get_file_content(working_directory, file_path):
    abs_work_dir = os.path.abspath(working_directory)
    file = os.path.abspath(os.path.join(abs_work_dir, file_path))

    if not file.startswith(abs_work_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(file, 'r') as file:
            content = file.read()
            if len(content) > 10000:
                content = content[:10000] + '[...File "{file_path}" truncated at 10000 characters]'
            return content
    except OSError as e:
        return f'Error reading file "{file_path}": {e.strerror}'
    except Exception as e:
        return f'An unexpected error occurred while reading file "{file_path}": {e}'
