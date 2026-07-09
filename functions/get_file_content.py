import os

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