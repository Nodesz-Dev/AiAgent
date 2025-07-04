import os.path
import subprocess
from google import genai
from google.genai import types

def run_python_file(working_directory, file_path, args=None):

    try:
        if file_path.startswith("/"):
            return f"Error: {file_path} is an absolute path, cannot pass in an absolute path as second arguement"

        absolute_working_path = os.path.abspath(working_directory)
        joined_file = os.path.join(working_directory, file_path)
        absolute_file_path = os.path.abspath(joined_file)

        if not absolute_file_path.startswith(absolute_working_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(absolute_file_path):
            return f'Error: File "{file_path}" not found.'
        
        root, extension = os.path.splitext(os.path.basename(absolute_file_path))

        if extension != ".py":
            return f'Error: "{file_path}" is not a Python file.'
        
        try:
            commands = ["python3", absolute_file_path]

            if args:
                commands.append(args)

            code_result = subprocess.run(commands,  cwd=absolute_working_path,
                                         check=True, capture_output=True, text=True, timeout=30)
            
            output = []
            if code_result.stdout:
                output.append(f"STDOUT: {code_result.stdout}")
            if code_result.stderr:
                output.append(f"STDERR: {code_result.stderr}")
            if code_result.returncode != 0:
                output.append(f"Process exited with code {code_result.returncode}")

            return "\n".join(output) if output else "No output produced"

        except Exception as error:
            return f"Error: executing Python file: {error}"


    except Exception as error:
        return f"Error: {error}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python script at target file path, returning the results of the script being run, as well as any errors it encountered",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "File path": types.Schema(
                type=types.Type.STRING,
                description="The path to the target python script we wish to execute, relative to the working directory. If path is not given, nothing will be executed",
            ),
            "Args": types.Schema(
                type=types.Type.STRING,
                description = "Optional arguements that will be passed to through to the target python script being ran"
            )
        },
    ),
)