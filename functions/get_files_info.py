import os
from openai.types.chat import ChatCompletionToolUnionParam

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        workdir_abs_path: str = os.path.abspath(working_directory)
        dir_path: str = os.path.normpath(os.path.join(workdir_abs_path, directory))
        valid_directory: bool = os.path.commonpath([dir_path, workdir_abs_path]) == workdir_abs_path
        if not valid_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(dir_path):
            return f'Error: "{directory}" is not a directory'
        else:
            files_list: list[str] = []
            for file in os.scandir(dir_path):
                file_stat: os.stat_result = file.stat()
                files_list.append(f"- {file.name}: file_size={file_stat.st_size} bytes, is_dir={file.is_dir()}")
            return '\n'.join(files_list)
    except Exception as e:
        return f"Error: {type(e).__name__} exception occurred: {e}"

schema_get_files_info: ChatCompletionToolUnionParam = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}