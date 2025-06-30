import os.path

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