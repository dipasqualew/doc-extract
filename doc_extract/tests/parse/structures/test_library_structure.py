"""
Tests for LibraryStructure
module: doc_extract.parse.structures
"""
from unittest.mock import patch
import pytest
from doc_extract.parse.objects import ParsedModule, ParsedClass, ParsedFunction
from doc_extract.parse.structures import CodeStructure, LibraryStructure, ModuleStructure
from doc_extract.tests.mixins import RecursiveTempDirectory, TempDirectory, repr_should_be_defined, str_should_be_defined, create_node
from doc_extract.tests.nodes import (
    create_module_node,
    create_class_node,
    create_function_node,
)
from doc_extract.tests.paths import FOLDER_PATHS_NAME_PAIRS, FOLDER_PATHS


def test_is_subclass():
    """Is it instance of CodeStructure"""
    assert issubclass(LibraryStructure, CodeStructure)

@pytest.mark.parametrize("library_path,name", FOLDER_PATHS_NAME_PAIRS)
def test_init(library_path, name):
    """__init__ creates the expected object"""
    definitions = [
        {
            "dir_suffix": path,
        }
        for path in library_path.split("/")
    ]
    with RecursiveTempDirectory(definitions) as refs:
        structure = LibraryStructure(refs[-1][0])
        assert structure.library_name.endswith(name)
        assert structure.library_path == refs[-1][0]
        assert structure.module_paths == []
        assert structure.modules == []

@pytest.mark.parametrize("library_path", FOLDER_PATHS)
def test_repr(library_path):
    """__repr__ should be defined"""
    definitions = [
        {
            "dir_suffix": path,
        }
        for path in library_path.split("/")
    ]
    with RecursiveTempDirectory(definitions) as refs:
        structure = LibraryStructure(refs[-1][0])
        obj_repr = repr_should_be_defined(structure)
        assert obj_repr == f"<Library '{structure.library_name}' at '{structure.library_path}'>"

@pytest.mark.parametrize("library_path", FOLDER_PATHS)
def test_str(library_path):
    """__str__ should be defined"""
    definitions = [
        {
            "dir_suffix": path,
        }
        for path in library_path.split("/")
    ]
    with RecursiveTempDirectory(definitions) as refs:
        structure = LibraryStructure(refs[-1][0])
        obj_str = str_should_be_defined(structure)
        assert obj_str == f"Library '{structure.library_name}' at '{structure.library_path}'"


@pytest.mark.parametrize("n_functions", (0, 1, 2, 3))
@pytest.mark.parametrize("n_classes", (0, 1, 2, 3))
@patch("doc_extract.parse.structures.ast.walk")
def test_parse_module(walk_mock, n_classes, n_functions):
    """Parses a module and creates a ModuleStructure"""
    module_node = create_module_node()
    class_nodes = [create_class_node() for _ in range(n_classes)]
    function_nodes = [create_function_node() for _ in range(n_functions)]
    nodes = [module_node] + class_nodes + function_nodes + [create_node(),]
    walk_mock.return_value = nodes

    with TempDirectory(file_suffixes=["module"]) as refs:
        library_structure = LibraryStructure(refs[0])
        module_structure = library_structure.parse_module(refs[1][0])
        assert module_structure.module == ParsedModule(module_node, library_structure.library_path)
        assert module_structure.classes == [ ParsedClass(node) for node in class_nodes ]
        assert module_structure.functions == [ ParsedFunction(node) for node in function_nodes ]

@pytest.mark.parametrize("module_paths", (
    (),
    ("module1"),
    ("module1", "module2", "module3"),
))
def test_serialize(module_paths):
    """Serializer the LibraryStructure"""
    with TempDirectory() as refs:
        modules = [
            ModuleStructure(path)
            for path in module_paths
        ]

        library_structure = LibraryStructure(refs[0])
        library_structure.modules = modules

        expected = {
            "library_path": library_structure.library_path,
            "modules": [
                module_structure.serialize()
                for module_structure in modules
            ]
        }

        assert library_structure.serialize() == expected
