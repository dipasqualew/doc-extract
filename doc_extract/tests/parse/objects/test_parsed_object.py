"""
Tests the ParsedObject class
module: doc_extract.parse.objects
"""
import ast
import pytest
from doc_extract.tests.mixins import create_node, repr_should_be_defined, str_should_be_defined
from doc_extract.parse.objects import ParsedObject

NODE_TYPES = (
    ast.Module,
    ast.ClassDef,
    ast.FunctionDef,
)

@pytest.mark.parametrize("node_type", NODE_TYPES)
def test_init(node_type):
    """__init__ sets all the expected properties"""
    node = create_node(node_type=node_type)
    obj = ParsedObject(node)
    assert obj.node == node
    assert obj.docstring == ast.get_docstring(node)
    assert obj.name == "Unknown type"

@pytest.mark.parametrize("node_type", NODE_TYPES)
def test_serialize(node_type):
    """Serialized returns the expected dict"""
    node = create_node(node_type=node_type)
    obj = ParsedObject(node)
    serialized = obj.serialize()
    expected = {
        "name": "Unknown type",
        "docstring": ast.get_docstring(node),
    }
    assert isinstance(serialized, dict)
    assert serialized == expected

@pytest.mark.parametrize("node_type", NODE_TYPES)
def test_repr(node_type):
    """__repr__ should be defined"""
    node = create_node(node_type=node_type)
    obj = ParsedObject(node)
    obj_repr = repr_should_be_defined(obj)
    assert obj_repr == "<Object: 'Unknown type'>"

@pytest.mark.parametrize("node_type", NODE_TYPES)
def test_str(node_type):
    """__str__ should be defined"""
    node = create_node(node_type=node_type)
    obj = ParsedObject(node)
    obj_str = str_should_be_defined(obj)
    assert obj_str == "Object: 'Unknown type'"
