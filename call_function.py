import functions.get_files_info as get_files_info
import functions.get_file_content as get_file_content
import functions.run_python_file as run_python_file
import functions.write_file_content as write_file_content
import json
from collections.abc import Callable

available_functions = [
    get_files_info.schema_get_files_info,
    get_file_content.schema_get_file_content,
    run_python_file.schema_run_python_file,
    write_file_content.schema_write_file_content
]

def call_function(tool_call, verbose: bool = False) -> dict:
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")
    function_args["working_directory"] = "./calculator"
    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    function_map: dict[str, Callable[..., str]] = {
        "get_file_content": get_file_content.get_file_content,
        "get_files_info": get_files_info.get_files_info,
        "run_python_file": run_python_file.run_python_file,
        "write_file_content": write_file_content.write_file
    }

    if function_name not in function_map:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {function_name}",
        }
    result = function_map[function_name](**function_args)
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result,
    }
