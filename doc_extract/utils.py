"""
Library shared utils
"""
import os
from pathlib import Path


def get_python_sources_in_directory(directory):
    """
    Gets all the python source files in
    the directory and all subdirectories

    :param directory: str
    :returns: List<pathlib.Path>
    """
    result = [ str(path) for path in Path(directory).rglob("*.py") ]
    return result

def get_python_module_name_from_path(path):
    """
    Transforms a filesystem path
    into a python module path

    :param path: str
    :returns: str
    """
    return (
        path
        .replace(".py", "")
        .replace(os.path.sep, ".")
        .strip(".")
    )

def get_python_name_from_path(path):
    """
    Transforms a filesystem path into a modular name
    (i.e. the last bit of the python module path)

    :param path: str
    :returns: str
    """
    return (
        get_python_module_name_from_path(path)
        .split(".")
        .pop()
    )
