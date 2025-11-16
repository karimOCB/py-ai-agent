import os
import sys
from google import genai
from dotenv import load_dotenv

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    if len(sys.argv) <= 1:
        print("A prompt is needed to continue")
        sys.exit(1)
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=sys.argv[1])
    print(f"""
        Here: {response.text}
        Prompt tokens: {response.usage_metadata.prompt_token_count}
        Response tokens: {response.usage_metadata.candidates_token_count}
    """)

if __name__ == "__main__":
    main()
