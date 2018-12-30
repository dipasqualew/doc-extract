import os
from pathlib import Path


def get_python_sources_in_directory(directory):
    result = list(Path(directory).rglob("*.py"))
    return result

def get_python_module_name_form_path(path):
    return (
        path
        .replace(".py", "")
        .replace(os.path.sep, ".")
        .strip(".")
    )
