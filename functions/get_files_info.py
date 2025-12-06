import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    dir_path = os.path.abspath(os.path.join(abs_working_dir, directory))

    if not dir_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(dir_path):
        return f'Error: "{directory}" is not a directory'

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


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)