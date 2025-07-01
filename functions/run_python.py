import os.path
import subprocess

def run_python_file(working_directory, file_path):

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
            code_result = subprocess.run(["python3", absolute_file_path],  cwd=absolute_working_path,
                                         check=True, capture_output=True, text=True, timeout=30)
            
            if code_result.stdout == None:
                return "No output produced"
            
            print(code_result.stderr)

            return "\n".join([f"STDOUT: {code_result.stdout}", f"STDERR: {code_result.stderr}"])

        except subprocess.CalledProcessError as error:
            return f"Process exited with code {error.returncode}"
        except Exception as error:
            return f"Error: executing Python file: {error}"


    except Exception as error:
        return f"Error: {error}"