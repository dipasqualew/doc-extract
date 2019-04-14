"""
Paths for path functions and parametrized tests
"""
from doc_extract.tests.th.os import _get_os_specific_path, _get_os_specific_paths

DEFAULT_PATH = _get_os_specific_path("module1/module2/module3")

DEFAULT_NAME = _get_os_specific_path("module1.module2.module3")

PATH_PREFIXES = _get_os_specific_paths("", "/", "./", "../")

PATH_MODULE_PAIRS = (
    _get_os_specific_paths("__init__.py", "__init__"),
    _get_os_specific_paths("module.py", "module"),
    _get_os_specific_paths("module/__init__.py", "module.__init__"),
    _get_os_specific_paths(DEFAULT_PATH, DEFAULT_NAME),
)

PATH_ABSOLUTE_MODULE_PAIRS = (
    _get_os_specific_paths("__init__.py", "__init__"),
    _get_os_specific_paths("module.py", "module"),
    _get_os_specific_paths("module/__init__.py", "__init__"),
    _get_os_specific_paths(DEFAULT_PATH, "module3"),
)

FOLDER_PATHS_NAME_PAIRS = (
    _get_os_specific_paths("folder_1", "folder_1"),
    _get_os_specific_paths("folder_2/folder_3", "folder_3"),
    _get_os_specific_paths("folder_4/folder_5/folder_6", "folder_6"),
)

PATHS = tuple(pair[0] for pair in PATH_MODULE_PAIRS)
FOLDER_PATHS = tuple(pair[0] for pair in FOLDER_PATHS_NAME_PAIRS)
