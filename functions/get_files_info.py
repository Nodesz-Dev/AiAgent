import os.path

def get_files_info(working_directory, directory=None):

    if directory.startswith("/"):
        return f"Error: {directory} is an absolute path, cannot pass in an absolute path as second arguement"

    absolute_working_directory = os.path.abspath(working_directory)
    absolute_directory = ""
    if directory == ".":
        absolute_directory = absolute_working_directory
    else:
        absolute_directory = os.path.join(absolute_working_directory, directory)
    
    if not os.path.exists(absolute_directory) or directory.startswith(".."):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(absolute_directory):
        return f'Error: "{directory}" is not a directory'
    
    list_of_file_in_directory = os.listdir(absolute_directory)
    list_of_file_info = []

    for item in list_of_file_in_directory:
        item_size = os.path.getsize(os.path.join(absolute_directory, item))
        item_isdir = os.path.isdir(os.path.join(absolute_directory, item))
        item_info_string = f"- {item}: file size={item_size} bytes, is_dir={item_isdir}"

        list_of_file_info.append(item_info_string)

    return "\n".join(list_of_file_info)