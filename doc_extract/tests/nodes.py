"""
Generates nodes to be used in tests
"""
import ast
from doc_extract.tests.mixins import create_node


# Typical node types
NODE_TYPES = (
    ast.Module,
    ast.ClassDef,
    ast.FunctionDef,
)

# Typical function nodes
FUNCTION_NODES = (
    create_node(node_type=ast.FunctionDef),
    create_node(node_type=ast.FunctionDef, name=""),
    create_node(node_type=ast.FunctionDef, name="FUNCTION"),
    create_node(node_type=ast.FunctionDef, body=(create_node(),)),
    create_node(node_type=ast.FunctionDef, body=(create_node(), create_node())),
    create_node(node_type=ast.FunctionDef, name="FUNCTION_WITH_BODY", body=(create_node(),)),
)

CLASS_NODES = (
    create_node(node_type=ast.ClassDef),
    create_node(node_type=ast.ClassDef, name=""),
    create_node(node_type=ast.ClassDef, name="CLASS"),
    create_node(node_type=ast.ClassDef, body=(create_node(),)),
    create_node(node_type=ast.ClassDef, body=FUNCTION_NODES[:1]),
    create_node(node_type=ast.ClassDef, body=(create_node(),) + FUNCTION_NODES[:1]),
    create_node(node_type=ast.ClassDef, body=FUNCTION_NODES[:3]),
    create_node(node_type=ast.ClassDef, body=(create_node(),) + FUNCTION_NODES[:3]),
    create_node(node_type=ast.ClassDef, body=FUNCTION_NODES[:]),
    create_node(node_type=ast.ClassDef, body=(create_node(),) + FUNCTION_NODES[:]),
    create_node(node_type=ast.ClassDef, name="CLASS_WITH_METHODS_1", body=FUNCTION_NODES[:1]),
    create_node(node_type=ast.ClassDef, name="CLASS_WITH_METHODS_1", body=FUNCTION_NODES[:1] + (create_node(),)),
    create_node(node_type=ast.ClassDef, name="CLASS_WITH_METHODS_2", body=FUNCTION_NODES[:]),
    create_node(node_type=ast.ClassDef, name="CLASS_WITH_METHODS_2", body=FUNCTION_NODES[:] + (create_node(),)),
)


ALL_NODES = FUNCTION_NODES + CLASS_NODES
