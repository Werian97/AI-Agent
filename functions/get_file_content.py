import os

from openai.types.chat import ChatCompletionToolUnionParam

from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        workdir_abs_path: str = os.path.abspath(working_directory)
        file_path_abs: str = os.path.normpath(os.path.join(workdir_abs_path, file_path))
        valid_directory: bool = os.path.commonpath([file_path_abs, workdir_abs_path]) == workdir_abs_path
        if not valid_directory:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(file_path_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            with open(file_path_abs) as f:
                content: str = f.read(MAX_CHARS)
                if f.read(1):
                    content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return content
            
    except Exception as e:
        return f"Error: {type(e).__name__} exception occurred: {e}"
    
schema_get_file_content: ChatCompletionToolUnionParam = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "given a file path the function read and returns the content of a file. If the file is a directory it returns an error message instead",
        "parameters": {
            "type": "object",
            "required": ["file_path"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "the file path to the file that we want to get the content of",
                },
            },
        },
    },
}