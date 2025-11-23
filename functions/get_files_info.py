import os

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    dir_path = os.path.abspath(os.path.join(abs_working_dir, directory))
    print(dir_path)

    if not dir_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(dir_path):
        return f'Error: "{directory}" is not a directory'
    print(os.listdir(dir_path))

    output_lines = []

    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        try:
            size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            output_lines.append(f'- {file}: file_size={size} bytes, is_dir={is_dir}')       
        except OSError as e:
            output_lines.append(f'Error: Could not retrieve info for "{file}". {e.strerror}')
 
    return "\n".join(output_lines)