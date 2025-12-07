import os
import argparse
import sys

from google import genai
from google.genai import types
from dotenv import load_dotenv

from functions.generate_content import generate_content
from config import MAX_ITERS


def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
    
    i = 0
    while True:
        i += 1
        if i > MAX_ITERS:
            print(f"max iterations ({MAX_ITERS}) reached")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break 
        except Exception as e:
            print(f"Error in generate_content: {e}")

if __name__ == "__main__":
    main()
