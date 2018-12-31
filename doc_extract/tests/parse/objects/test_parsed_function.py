"""
Tests the ParsedFunction class
module: doc_extract.parse.objects
"""
import ast
import pytest
from doc_extract.tests.mixins import create_node, repr_should_be_defined, str_should_be_defined
from doc_extract.parse.objects import ParsedFunction


TEST_NODES = (
    create_node(node_type=ast.FunctionDef),
    create_node(node_type=ast.FunctionDef, name=""),
    create_node(node_type=ast.FunctionDef, name="FUNCTION"),
    create_node(node_type=ast.FunctionDef, body=[create_node()]),
    create_node(node_type=ast.FunctionDef, body=[create_node(), create_node()]),
    create_node(node_type=ast.FunctionDef, name="FUNCTION_WITH_BODY", body=[create_node()]),
)

@pytest.mark.parametrize("node", TEST_NODES)
def test_init(node):
    """__init__ sets all the expected properties"""
    obj = ParsedFunction(node)
    assert obj.node == node
    assert obj.docstring == ast.get_docstring(node)
    assert obj.name == node.name

@pytest.mark.parametrize("node", TEST_NODES)
def test_serialize(node):
    """Serialized returns the expected dict"""
    obj = ParsedFunction(node)
    serialized = obj.serialize()
    expected = {
        "name": node.name,
        "docstring": ast.get_docstring(node),
    }
    assert isinstance(serialized, dict)
    assert serialized == expected

@pytest.mark.parametrize("node", TEST_NODES)
def test_repr(node):
    """__repr__ should be defined"""
    obj = ParsedFunction(node)
    obj_repr = repr_should_be_defined(obj)
    assert obj_repr == f"<Function: '{node.name}'>"

@pytest.mark.parametrize("node", TEST_NODES)
def test_str(node):
    """__str__ should be defined"""
    obj = ParsedFunction(node)
    obj_str = str_should_be_defined(obj)
    assert obj_str == f"Function: '{node.name}'"
