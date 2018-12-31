"""
Tests the ParsedModule class
module: doc_extract.parse.objects
"""
import ast
import pytest
from doc_extract.tests.mixins import repr_should_be_defined, str_should_be_defined
from doc_extract.tests.nodes import MODULE_NODES
from doc_extract.parse.objects import ParsedModule

DEFAULT_PATH = "module1/module2/module3"
DEFAULT_NAME = "module1.module2.module3"

@pytest.mark.parametrize("path,name", (
    ("__init__.py", "__init__"),
    ("module.py", "module"),
    ("module/__init__.py", "module.__init__"),
    (DEFAULT_PATH, DEFAULT_NAME),
))
@pytest.mark.parametrize("path_prefix", ("", "/", "./", "../"))
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
