import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    if len(sys.argv) <= 1:
        print("A prompt is needed to continue")
        sys.exit(1)
    messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])])
    ]
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages)
    verbose_details = ""
    if "--verbose" in sys.argv:
        verbose_details = f"""
            User prompt: {sys.argv[2]}
            Prompt tokens: {response.usage_metadata.prompt_token_count}
            Response tokens: {response.usage_metadata.candidates_token_count}
        """
    print(f"""
        {response.text}
        {verbose_details}
    """)

if __name__ == "__main__":
    main()
