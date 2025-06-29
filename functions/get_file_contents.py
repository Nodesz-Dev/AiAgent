import os.path

MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
    
    absolute_working_path = os.path.abspath(working_directory)
    joined_file = os.path.join(working_directory, file_path)
   # print(joined_file)
    absolute_file_path = os.path.abspath(joined_file)
   # print(absolute_file_path)
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

    