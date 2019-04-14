"""
Tests the utils functions
module: doc_extract.utils
"""
import pytest
from doc_extract.tests.th.os import _get_os_specific_paths
from doc_extract.tests.th.files import TempDirectory
from doc_extract.utils import (
    get_python_sources_in_directory,
    get_python_module_name_from_path,
    get_python_name_from_path,
)


LEVEL_1_FILES = (
    (),
    ("level_1_1.py",),
    ("level_1_1.py", "level_1_2.py",),
)

LEVEL_2_FILES = (
    (),
    ("level_2_1.py",),
    ("level_2_1.py", "level_2_2.py",),
)

LEVEL_3_FILES = (
    (),
    ("__init__.py",),
    ("__init__.py", "module.py",),
)

NON_PYTHON_FILE_PATHS = (
    (),
    ("some_file",),
    ("some_pyc.pyc",),
    ("file_with_py",),
    ("file_with_py.txt",),
    ("some_file", "some_pyc.pyc", "file_with_py", "file_with_py.txt",),
)

def do_find_files_and_assert(original_folder, py_files):
    """
    Finds the python files in the original_folder
    then matches with the expected py_files
    """
    found_files = get_python_sources_in_directory(original_folder)
    assert len(found_files) == len(py_files)

    for py_file in py_files:
        py_file_found = False

        for found_file in found_files:
            if py_file in str(found_file):
                py_file_found = True
                break

        assert py_file_found

@pytest.mark.parametrize("non_py_files", NON_PYTHON_FILE_PATHS)
@pytest.mark.parametrize("py_files", LEVEL_3_FILES)
def test_find_files_linear(py_files, non_py_files):
    """Finds all and only the defined python files"""
    all_files = py_files + non_py_files

    with TempDirectory(file_suffixes=all_files) as refs:
        do_find_files_and_assert(refs[0], py_files)

@pytest.mark.parametrize("non_py_files", NON_PYTHON_FILE_PATHS)
@pytest.mark.parametrize("level_3_files", LEVEL_3_FILES)
@pytest.mark.parametrize("level_2_files", LEVEL_2_FILES)
@pytest.mark.parametrize("level_1_files", LEVEL_1_FILES)
def test_find_files_recursive(level_1_files, level_2_files, level_3_files, non_py_files):
    """Finds all and only the defined python files in subfolders"""
    batch1 = level_1_files + non_py_files
    batch2 = level_2_files + non_py_files
    batch3 = level_3_files + non_py_files
    expected_files = level_1_files + level_2_files + level_3_files

    with TempDirectory(file_suffixes=batch1) as refs1:
        with TempDirectory(parent_dir=refs1[0], file_suffixes=batch2) as refs2:
            with TempDirectory(parent_dir=refs2[0], file_suffixes=batch3):
                do_find_files_and_assert(refs1[0], expected_files)

@pytest.mark.parametrize("prefix", _get_os_specific_paths("", "/", "./", "../"))
@pytest.mark.parametrize("path,expected_module_name", (
    _get_os_specific_paths("module.py", "module"),
    _get_os_specific_paths("underscored_module_name.py", "underscored_module_name"),
    _get_os_specific_paths("camelCasedModuleName.py", "camelCasedModuleName"),
    _get_os_specific_paths("PascalCasedModuleName.py", "PascalCasedModuleName"),
    _get_os_specific_paths("some/module.py", "some.module"),
    _get_os_specific_paths("__init__.py", "__init__"),
    _get_os_specific_paths("some/__init__.py", "some.__init__"),
    _get_os_specific_paths("three/level/module.py", "three.level.module"),
    _get_os_specific_paths("three/level/__init__.py", "three.level.__init__"),
))
def test_get_python_module_name_from_path(path, expected_module_name, prefix):
    """The actual module name matches the expected module name"""
    actual_module_name = get_python_module_name_from_path(prefix + path)
    assert actual_module_name == expected_module_name

@pytest.mark.parametrize("prefix", _get_os_specific_paths("", "/", "./", "../"))
@pytest.mark.parametrize("path,expected_module_name", (
    _get_os_specific_paths("module.py", "module"),
    _get_os_specific_paths("underscored_module_name.py", "underscored_module_name"),
    _get_os_specific_paths("camelCasedModuleName.py", "camelCasedModuleName"),
    _get_os_specific_paths("PascalCasedModuleName.py", "PascalCasedModuleName"),
    _get_os_specific_paths("some/module.py", "module"),
    _get_os_specific_paths("__init__.py", "__init__"),
    _get_os_specific_paths("some/__init__.py", "__init__"),
    _get_os_specific_paths("three/level/module.py", "module"),
    _get_os_specific_paths("three/level/__init__.py", "__init__"),
))
def test_get_python_name_from_path(path, expected_module_name, prefix):
    """The actual module name matches the expected module name"""
    actual_module_name = get_python_name_from_path(prefix + path)
    assert actual_module_name == expected_module_name
