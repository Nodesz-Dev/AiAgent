import sys
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types
client = genai.Client(api_key=api_key)

import llm_config
from functions.call_function import call_function

def main():
    verbose = False

    if "--verbose" in sys.argv:
        verbose = True

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

    function_call_result = None
    if response.function_calls == None:
        print(response.text)
    else:
        function_call_result = call_function(response.function_calls[0], verbose)

    if function_call_result.parts[0].function_response.response:
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        raise Exception(f"Fatal error: function is missing returned response")

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

main()