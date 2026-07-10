import os
import subprocess

from openai.types.chat import ChatCompletionToolUnionParam

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        wd_abspath: str = os.path.abspath(working_directory)
        fp_abspath: str = os.path.normpath(os.path.join(wd_abspath, file_path))
        valid_path: bool = os.path.commonpath([wd_abspath, fp_abspath]) == wd_abspath
        if not valid_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not (os.path.exists(fp_abspath) and os.path.isfile(fp_abspath)):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not has_python_extension(file_path):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", fp_abspath]
        if args is not None:
            command.extend(args)
        
        process: subprocess.CompletedProcess = subprocess.run(command, text=True, capture_output=True, timeout=30)
        if process.returncode != 0:
            return f"Process exited with code {process.returncode}"
        
        if process.stderr == None and process.stdout == None:
            return "No output produced"
        
        output: str = f'STDOUT: {process.stdout}\n\
STDERR: {process.stderr}'
        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"

def has_python_extension(file_name: str):
    rev_file_name = file_name[::-1]
    return "yp." == rev_file_name[0:3]


schema_run_python_file: ChatCompletionToolUnionParam = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "execute or run the file specified with the file path. Additionally we can pass arguments if the file need them. If the file is a directory or it has not .py extension, it returns an error message instead",
        "parameters": {
            "type": "object",
            "required": ["file_path"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "the file path to the file that we want to execute",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "the arguments we want to pass for the file execution"
                }
            },
        },
    },
}