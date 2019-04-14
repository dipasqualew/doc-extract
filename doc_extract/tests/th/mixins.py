"""
Mixin test utils
"""
import ast


def create_node(node_type=None, **kwargs):
    """Creates an ast.Node"""
    if node_type is None:
        node_type = ast.Expression

    name = kwargs.get("name", "node_name")
    body = kwargs.get("body", ())

    node = node_type()
    setattr(node, "name", name)
    setattr(node, "body", body)

    return node

def repr_should_be_defined(obj):
    """Checks the obj.__repr__() method is properly defined"""
    obj_repr = repr(obj)

    assert isinstance(obj_repr, str)
    assert obj_repr == obj.__repr__()
    assert obj_repr.startswith("<")
    assert obj_repr.endswith(">")

    return obj_repr

def str_should_be_defined(obj):
    """Checks the obj.__str__() method is property defined"""
    obj_str = str(obj)

    assert isinstance(obj_str, str)
    assert obj_str == obj.__str__()
    assert obj_str

    return obj_str
