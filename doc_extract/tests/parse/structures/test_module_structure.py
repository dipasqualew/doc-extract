"""
Tests for ModuleStructure
module: doc_extract.parse.structures
"""
import pytest
from doc_extract.parse.objects import ParsedModule, ParsedClass, ParsedFunction
from doc_extract.parse.structures import CodeStructure, ModuleStructure
from doc_extract.tests.th.mixins import repr_should_be_defined, str_should_be_defined
from doc_extract.tests.nodes import (
    MODULE_NODES,
    CLASS_NODES,
    FUNCTION_NODES,
    get_node_functions,
    create_module_node,
    create_class_node,
    create_function_node,
)
from doc_extract.tests.paths import PATH_PREFIXES, PATH_MODULE_PAIRS, PATHS, DEFAULT_PATH


def test_is_subclass():
    """Is it instance of CodeStructure"""
    assert issubclass(ModuleStructure, CodeStructure)

@pytest.mark.parametrize("path,name", PATH_MODULE_PAIRS)
@pytest.mark.parametrize("path_prefix", PATH_PREFIXES)
def test_init(path_prefix, path, name):
    """__init__ creates the expected object"""
    module_path = path_prefix + path
    structure = ModuleStructure(module_path)
    assert structure.name == name
    assert structure.path == module_path
    assert structure.module is None
    assert structure.classes == []
    assert structure.functions == []
    assert structure.parsed_references == []

@pytest.mark.parametrize("path", PATHS)
@pytest.mark.parametrize("path_prefix", PATH_PREFIXES)
def test_repr(path_prefix, path):
    """__repr__ should be defined"""
    module_path = path_prefix + path
    structure = ModuleStructure(module_path)
    obj_repr = repr_should_be_defined(structure)
    assert obj_repr == f"<Module '{structure.name}' structure>"

@pytest.mark.parametrize("path", PATHS)
@pytest.mark.parametrize("path_prefix", PATH_PREFIXES)
def test_str(path_prefix, path):
    """__str__ should be defined"""
    module_path = path_prefix + path
    structure = ModuleStructure(module_path)
    obj_str = str_should_be_defined(structure)
    assert obj_str == f"Module '{structure.name}' structure"

@pytest.mark.parametrize("node", MODULE_NODES)
def test_parse_module(node):
    """Checks the module is parsed and added to the references"""
    structure = ModuleStructure(DEFAULT_PATH)
    structure.parse_module(node)
    assert structure.module == ParsedModule(node, DEFAULT_PATH)
    assert structure.parsed_references == [node]

@pytest.mark.parametrize("node", CLASS_NODES)
def test_parse_class(node):
    """Checks the class and its methods are parsed and added to the references"""
    structure = ModuleStructure(DEFAULT_PATH)
    structure.parse_class(node)
    expected_references = [node] + get_node_functions(node)
    assert structure.classes == [ParsedClass(node)]
    assert structure.functions == []
    assert structure.parsed_references == expected_references

@pytest.mark.parametrize("node", CLASS_NODES)
def test_parse_class_skip(node):
    """Checks the class is not parsed when its node is already in the references"""
    structure = ModuleStructure(DEFAULT_PATH)
    structure.parsed_references.append(node)
    structure.parse_class(node)
    assert structure.classes == []
    assert structure.functions == []

@pytest.mark.parametrize("node", FUNCTION_NODES)
def test_parse_function(node):
    """Checks the function is parsed and added to the references"""
    structure = ModuleStructure(DEFAULT_PATH)
    structure.parse_function(node)
    assert structure.classes == []
    assert structure.functions == [ParsedFunction(node)]
    assert structure.parsed_references == [node]

@pytest.mark.parametrize("node", FUNCTION_NODES)
def test_parse_function_skip(node):
    """Checks the function is not parsed when its node is already in the references"""
    structure = ModuleStructure(DEFAULT_PATH)
    structure.parsed_references.append(node)
    structure.parse_function(node)
    assert structure.classes == []
    assert structure.functions == []

@pytest.mark.parametrize("n_functions", (0, 1, 2, 3))
@pytest.mark.parametrize("n_classes", (0, 1, 2, 3))
@pytest.mark.parametrize("has_module", (True, False))
def test_serialize(has_module, n_classes, n_functions):
    """Checks the serialization is properly populated"""
    structure = ModuleStructure(DEFAULT_PATH)

    if has_module:
        structure.parse_module(create_module_node())

    for _ in range(n_classes):
        structure.parse_class(create_class_node())

    for _ in range(n_functions):
        structure.parse_function(create_function_node())

    assert (structure.module is not None) == has_module
    assert len(structure.classes) == n_classes
    assert len(structure.functions) == n_functions

    expected = {
        "module": structure.module.serialize() if has_module else None,
        "classes": [ parsed_class.serialize() for parsed_class in structure.classes ],
        "functions": [ parsed_function.serialize() for parsed_function in structure.functions ],
    }

    assert structure.serialize() == expected
