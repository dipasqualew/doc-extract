"""
Tests the ParsedObject class
module: doc_extract.parse.objects
"""
import ast
import pytest
from doc_extract.tests.th.mixins import repr_should_be_defined, str_should_be_defined
from doc_extract.tests.nodes import ALL_NODES
from doc_extract.parse.objects import ParsedObject


@pytest.mark.parametrize("node", ALL_NODES)
def test_init(node):
    """__init__ sets all the expected properties"""
    obj = ParsedObject(node)
    assert obj.node == node
    assert obj.docstring == ast.get_docstring(node)
    assert obj.name == "Unknown type"

@pytest.mark.parametrize("node", ALL_NODES)
def test_serialize(node):
    """Serialized returns the expected dict"""
    obj = ParsedObject(node)
    serialized = obj.serialize()
    expected = {
        "name": "Unknown type",
        "docstring": ast.get_docstring(node),
    }
    assert isinstance(serialized, dict)
    assert serialized == expected

@pytest.mark.parametrize("node", ALL_NODES)
def test_repr(node):
    """__repr__ should be defined"""
    obj = ParsedObject(node)
    obj_repr = repr_should_be_defined(obj)
    assert obj_repr == "<Object: 'Unknown type'>"

@pytest.mark.parametrize("node", ALL_NODES)
def test_str(node):
    """__str__ should be defined"""
    obj = ParsedObject(node)
    obj_str = str_should_be_defined(obj)
    assert obj_str == "Object: 'Unknown type'"

@pytest.mark.parametrize("node", ALL_NODES)
def test_eq(node):
    """__eq__ should be defined"""
    obj1 = ParsedObject(node)
    obj2 = ParsedObject(node)
    assert id(obj1) != id(obj2)
    assert obj1 == obj2
