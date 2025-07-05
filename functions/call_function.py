import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

working_directory = os.environ.get("WORKING_DIRECTORY")

def call_function(function_call_part:types.FunctionCall, verbose=False):

    function_call_part.args["working_directory"] = working_directory

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_dict = {
        "get_files_info" : get_files_info,
        "get_file_content" : get_file_content,
        "write_file" : write_file,
        "run_python_file" : run_python_file
    }

    function_result = None
    #function call
    try:
        function_result = function_dict[function_call_part.name](**function_call_part.args)
        print(function_result)
    except NameError:
        print(f"function name not found in dict {function_call_part.name}")
    except:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": function_result },
        )
    ],
)