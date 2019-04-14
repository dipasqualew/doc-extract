"""
Tests the ParsedModule class
module: doc_extract.parse.objects
"""
import ast
import pytest
from doc_extract.tests.th.mixins import repr_should_be_defined, str_should_be_defined
from doc_extract.tests.nodes import MODULE_NODES
from doc_extract.tests.paths import DEFAULT_NAME, DEFAULT_PATH, PATH_PREFIXES, PATH_MODULE_PAIRS
from doc_extract.parse.objects import ParsedModule


@pytest.mark.parametrize("path,name", PATH_MODULE_PAIRS)
@pytest.mark.parametrize("path_prefix", PATH_PREFIXES)
@pytest.mark.parametrize("node", MODULE_NODES)
def test_init(node, path_prefix, path, name):
    """__init__ sets all the expected properties"""
    module_path = path_prefix + path
    obj = ParsedModule(node, module_path)
    assert obj.node == node
    assert obj.name == name
    assert obj.path == module_path
    assert obj.docstring == ast.get_docstring(node)

@pytest.mark.parametrize("node", MODULE_NODES)
def test_serialize(node):
    """Serialized returns the expected dict"""
    obj = ParsedModule(node, DEFAULT_PATH)
    serialized = obj.serialize()
    expected = {
        "name": DEFAULT_NAME,
        "docstring": ast.get_docstring(node),
    }
    assert isinstance(serialized, dict)
    assert serialized == expected

@pytest.mark.parametrize("node", MODULE_NODES)
def test_repr(node):
    """__repr__ should be defined"""
    obj = ParsedModule(node, DEFAULT_PATH)
    obj_repr = repr_should_be_defined(obj)
    assert obj_repr == f"<Module at: '{DEFAULT_PATH}'>"

@pytest.mark.parametrize("node", MODULE_NODES)
def test_str(node):
    """__str__ should be defined"""
    obj = ParsedModule(node, DEFAULT_PATH)
    obj_str = str_should_be_defined(obj)
    assert obj_str == f"Module at: '{DEFAULT_PATH}'"

@pytest.mark.parametrize("node", MODULE_NODES)
def test_eq(node):
    """__eq__ should be defined"""
    obj1 = ParsedModule(node, DEFAULT_PATH)
    obj2 = ParsedModule(node, DEFAULT_PATH)
    assert id(obj1) != id(obj2)
    assert obj1 == obj2
