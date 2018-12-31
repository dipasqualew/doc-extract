"""
Tests the ParsedClass class
module: doc_extract.parse.objects
"""
import ast
import pytest
from doc_extract.tests.mixins import repr_should_be_defined, str_should_be_defined
from doc_extract.tests.nodes import CLASS_NODES
from doc_extract.parse.objects import ParsedClass, ParsedFunction

def get_node_functions(node):
    """Returns the nodes that are functions in node.body"""
    return [
        child_node
        for child_node in node.body
        if isinstance(child_node, ast.FunctionDef)
    ]

@pytest.mark.parametrize("node", CLASS_NODES)
def test_init(node):
    """__init__ sets all the expected properties"""
    obj = ParsedClass(node)
    assert obj.node == node
    assert obj.docstring == ast.get_docstring(node)
    assert obj.name == node.name
    assert len(obj.functions) == len(get_node_functions(node))

@pytest.mark.parametrize("node", CLASS_NODES)
def test_repr(node):
    """__repr__ should be defined"""
    obj = ParsedClass(node)
    obj_repr = repr_should_be_defined(obj)
    assert obj_repr == f"<Class: '{node.name}'>"

@pytest.mark.parametrize("node", CLASS_NODES)
def test_str(node):
    """__str__ should be defined"""
    obj = ParsedClass(node)
    obj_str = str_should_be_defined(obj)
    assert obj_str == f"Class: '{node.name}'"

@pytest.mark.parametrize("node", CLASS_NODES)
def test_eq(node):
    """__eq__ should be defined"""
    obj1 = ParsedClass(node)
    obj2 = ParsedClass(node)
    assert id(obj1) != id(obj2)
    assert obj1 == obj2

@pytest.mark.parametrize("node", CLASS_NODES)
def test_read_functions(node):
    """Reads the functions and generates ParsedFunctions"""
    obj = ParsedClass(node)
    expected_parsed_functions = [
        ParsedFunction(function_node)
        for function_node in get_node_functions(node)
    ]

    assert obj.read_functions(node.body) == expected_parsed_functions
    assert obj.functions == expected_parsed_functions

@pytest.mark.parametrize("node", CLASS_NODES)
def test_serialize(node):
    """Serialized returns the expected dict"""
    obj = ParsedClass(node)
    serialized = obj.serialize()
    expected = {
        "name": node.name,
        "docstring": ast.get_docstring(node),
        "methods": [ func.serialize() for func in obj.functions ],
    }
    assert isinstance(serialized, dict)
    assert serialized == expected
