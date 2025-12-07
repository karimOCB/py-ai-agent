from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from config import system_prompt
from google.genai import types
from functions.call_function import call_function

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file],
)

def generate_content(client, messages, verbose):       
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.candidates:
        for cand in response.candidates:
            messages.append(cand.content)

    if not response.function_calls and response.text:
        return response.text
        
    fn_responses = []
    for func_call in response.function_calls:
        result = call_function(func_call, verbose)
        part = result.parts[0]
        if not part.function_response or not part.function_response.response:
            raise Exception("Function call did not return a response")
        if verbose:
            print(f"-> {part.function_response.response}") 
        fn_responses.append(part)
        
    if not fn_responses:
        raise Exception("no function responses generated, exiting.")

    messages.append(types.Content(role="user", parts=fn_responses))

    return None