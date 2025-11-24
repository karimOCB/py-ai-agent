import subprocess, os

def run_python_file(working_directory, file_path, args=[]):
    abs_work_dir = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(abs_work_dir, file_path))
    
    if not abs_file.startswith(abs_work_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    cmd = ["python", abs_file] + args
  
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=30, cwd=abs_work_dir, text=True)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    if not result.stdout and not result.stderr:
        return "No output produced."
    
    formatted = f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}'
    if result.returncode != 0: 
        formatted += f" Process exited with code {result.returncode}"
    return formatted
