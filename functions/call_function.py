from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from google.genai import types 

def call_function(function_call_part, verbose=False):
    args = dict(function_call_part.args)
    args['working_directory'] = "./calculator"
    if "file" in args and "file_path" not in args:
        args["file_path"] = args.pop("file")
    tools = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,   
    }
    fn_name = function_call_part.name

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")
    
    if fn_name not in tools:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=fn_name,
                    response={"error": f"Unknown function: {fn_name}"},
                )
            ],
        )
    else: 
        fn = tools[function_call_part.name]
        result = fn(**args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=fn_name,
                    response={"result": result},
                )
            ],
        )
    




