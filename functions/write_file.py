import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        workdir_abs_path: str = os.path.abspath(working_directory)
        file_path_abs: str = os.path.normpath(os.path.join(workdir_abs_path, file_path))
        valid_directory: bool = os.path.commonpath([file_path_abs, workdir_abs_path]) == workdir_abs_path
        if not valid_directory:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(file_path_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        else:
            os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)
            with open(file_path_abs, "w") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


            
    except Exception as e:
        return f"Error: {type(e).__name__} exception occurred: {e}"