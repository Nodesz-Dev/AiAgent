import os.path
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):

    try:
        if file_path.startswith("/"):
            return f"Error: {file_path} is an absolute path, cannot pass in an absolute path as second arguement"

        absolute_working_path = os.path.abspath(working_directory)
        joined_file = os.path.join(working_directory, file_path)
        absolute_file_path = os.path.abspath(joined_file)

        if not absolute_file_path.startswith(absolute_working_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        try:
            os.makedirs(os.path.dirname(absolute_file_path), exist_ok=True)
        except FileExistsError:
            pass
        except Exception as error:
            return f"Error: {error} (1)"
        
        try:
            with open(absolute_file_path, "w") as f:
                f.write(content)
        except Exception as error:
            return f"Error: {error} (2)"
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as error:
        return f"Error: {error}"
    except:
        return f"Error: Something went wrong, error not specified"
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Takes a target file path, creating the directories and files if necessary then writes the given contents into the file returning a message of success",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "File path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the target file we wish to write to, relative to the working directory. If no file exists at this path, the necessary directories and files will be created before being writtin to",
            ),
            "Contents": types.Schema(
                type=types.Type.STRING,
                description="This is the text contents we wish to write to the designated file"
            )
        },
    ),
)