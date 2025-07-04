import os.path
from google import genai
from google.genai import types

MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
    try:
        if file_path.startswith("/"):
            return f"Error: {file_path} is an absolute path, cannot pass in an absolute path as second arguement"


        absolute_working_path = os.path.abspath(working_directory)
        joined_file = os.path.join(working_directory, file_path)
        absolute_file_path = os.path.abspath(joined_file)
        file_content_string = []

        if not absolute_file_path.startswith(absolute_working_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(absolute_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(absolute_file_path, "r") as f:
            file_content_string.append(f.read(MAX_CHARS))
            if len(f.read()) > MAX_CHARS:
                file_content_string.append(f'[...File "{file_path}" truncated at 10000 characters]') 

        return "\n".join(file_content_string)
    except Exception as error:
        return f"Error: {error}"
    except:
        return f"Error: Something went wrong, error not specified"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists content of the specified file up to a maximum of 10000 characters, given in text form. File must be within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "File path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the target file we wish to get the contents from, relative to the working directory. If path is not given, nothing will be retrieved",
            ),
        },
    ),
)
    