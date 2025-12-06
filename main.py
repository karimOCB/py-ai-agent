import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from config import system_prompt

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    available_functions = types.Tool(
        function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file],
    )
    if len(sys.argv) <= 1:
        print("A prompt is needed to continue")
        sys.exit(1)
    messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])])
    ]
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    verbose_details = ""
    if "--verbose" in sys.argv:
        verbose_details = f"""
            User prompt: {sys.argv[2]}
            Prompt tokens: {response.usage_metadata.prompt_token_count}
            Response tokens: {response.usage_metadata.candidates_token_count}
        """
    text = ""
    if response.function_calls != None:
        for func_call in response.function_calls:
            text += f"Calling function: {func_call.name}({func_call.args})\n"
    else:
        text += response.text  
    print(f"""
        {text}
        {verbose_details}
    """)

if __name__ == "__main__":
    main()
