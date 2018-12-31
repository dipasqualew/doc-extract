"""
Paths for path functions and parametrized tests
"""


DEFAULT_PATH = "module1/module2/module3"

DEFAULT_NAME = "module1.module2.module3"

PATH_PREFIXES = ("", "/", "./", "../")

PATH_MODULE_PAIRS = (
    ("__init__.py", "__init__"),
    ("module.py", "module"),
    ("module/__init__.py", "module.__init__"),
    (DEFAULT_PATH, DEFAULT_NAME),
)

PATH_ABSOLUTE_MODULE_PAIRS = (
    ("__init__.py", "__init__"),
    ("module.py", "module"),
    ("module/__init__.py", "__init__"),
    (DEFAULT_PATH, "module3"),
)

FOLDER_PATHS_NAME_PAIRS = (
    ("folder_1", "folder_1"),
    ("folder_2/folder_3", "folder_3"),
    ("folder_4/folder_5/folder_6", "folder_6"),
)

PATHS = tuple(pair[0] for pair in PATH_MODULE_PAIRS)
FOLDER_PATHS = tuple(pair[0] for pair in FOLDER_PATHS_NAME_PAIRS)
