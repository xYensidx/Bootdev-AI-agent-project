import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
     try:
          abs_working_dir = os.path.abspath(working_directory)
          target_dir = os.path.normpath(os.path.join(abs_working_dir, file_path))
          if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
               return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
          if not os.path.isfile(target_dir):
               return f'Error: "{file_path}" does not exist or is not a regular file'
          if not target_dir.endswith(".py"):
               return f'Error: "{file_path}" is not a Python file'
          command = ["python", target_dir]
          if args:
               command.extend(args)
          result = subprocess.run(
               command, 
               cwd=abs_working_dir, 
               capture_output=True, 
               text=True, 
               timeout=30,
          )
          output: list[str] = []
          if result.returncode != 0:
               output.append(f"Process exited with code {result.returncode}")
          if not result.stdout and not result.stderr:
               output.append(f"No output produced.")
          if result.stdout:
               output.append(f"STDOUT: {result.stdout}")
          if result.stderr:
               output.append(f"STDERR: {result.stderr}")
          return "\n".join(output)
          
     except Exception as e:
          return f"Error executing file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes the main Python file relative to the working directory with optional arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Arguments to pass to the Python file"
                }
            },
        },
    },
}
