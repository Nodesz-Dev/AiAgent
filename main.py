import sys
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types
client = genai.Client(api_key=api_key)

import llm_config

def main():

    if len(sys.argv) == 1:
        print("No prompt provided")
        sys.exit(1)
    
    user_prompt = sys.argv[1]
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config = types.GenerateContentConfig(tools=[llm_config.available_functions],
                                         system_instruction=llm_config.system_prompt)
    )

    if response.function_calls == None:
        print(response.text)
    else:
        print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")

    

    if len(sys.argv) == 3:
        if sys.argv[2] == "--verbose":
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

main()