import os

def write_file(working_directory, file_path, content):
    abs_work_dir = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(abs_work_dir, file_path))
    
    if not abs_file.startswith(abs_work_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file):
        try:
            os.makedirs(os.path.dirname(abs_file), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory {e}"
    
    if os.path.exists(abs_file) and os.path.isdir(abs_file):
        return f'Error: "{file_path}" is a directory, not a file'

    try:
        with open(abs_file, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'