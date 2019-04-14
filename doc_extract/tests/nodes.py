"""
Generates nodes to be used in tests
"""
import ast
from doc_extract.tests.th.mixins import create_node


# Typical node types
NODE_TYPES = (
    ast.Module,
    ast.ClassDef,
    ast.FunctionDef,
)

def create_function_node(**kwargs):
    """
    Creates a function node
    """
    return create_node(node_type=ast.FunctionDef, **kwargs)

def create_class_node(**kwargs):
    """
    Creates a class node
    """
    return create_node(node_type=ast.ClassDef, **kwargs)

def create_module_node(**kwargs):
    """
    Creates a module node
    """
    return create_node(node_type=ast.Module, **kwargs)

def get_node_functions(node):
    """Returns the nodes that are functions in node.body"""
    return [
        child_node
        for child_node in node.body
        if isinstance(child_node, ast.FunctionDef)
    ]

# Typical function nodes
FUNCTION_NODES = (
    create_function_node(),
    create_function_node(name=""),
    create_function_node(name="FUNCTION"),
    create_function_node(body=(create_node(),)),
    create_function_node(body=(create_node(), create_node())),
    create_function_node(name="FUNCTION_WITH_BODY", body=(create_node(),)),
)

CLASS_NODES = (
    create_class_node(),
    create_class_node(name=""),
    create_class_node(name="CLASS"),
    create_class_node(body=(create_node(),)),
    create_class_node(body=FUNCTION_NODES[:1]),
    create_class_node(body=(create_node(),) + FUNCTION_NODES[:1]),
    create_class_node(body=FUNCTION_NODES[:3]),
    create_class_node(body=(create_node(),) + FUNCTION_NODES[:3]),
    create_class_node(body=FUNCTION_NODES[:]),
    create_class_node(body=(create_node(),) + FUNCTION_NODES[:]),
    create_class_node(name="CLASS_WITH_METHODS_1", body=FUNCTION_NODES[:1]),
    create_class_node(name="CLASS_WITH_METHODS_1", body=FUNCTION_NODES[:1] + (create_node(),)),
    create_class_node(name="CLASS_WITH_METHODS_2", body=FUNCTION_NODES[:]),
    create_class_node(name="CLASS_WITH_METHODS_2", body=FUNCTION_NODES[:] + (create_node(),)),
)

MODULE_NODES = (
    create_module_node(),
    create_module_node(name=""),
    create_module_node(name="MODULE"),
    create_module_node(body=(create_node(),)),

    # Classes modules
    create_module_node(body=CLASS_NODES[:1]),
    create_module_node(body=(create_node(),) + CLASS_NODES[:1]),
    create_module_node(body=CLASS_NODES[:3]),
    create_module_node(body=(create_node(),) + CLASS_NODES[:3]),
    create_module_node(body=CLASS_NODES[:]),
    create_module_node(body=(create_node(),) + CLASS_NODES[:]),
    create_module_node(name="MODULE_WITH_CLASSES_1", body=CLASS_NODES[:1]),
    create_module_node(name="MODULE_WITH_CLASSES_2", body=CLASS_NODES[:1] + (create_node(),)),
    create_module_node(name="MODULE_WITH_CLASSES_3", body=CLASS_NODES[:]),
    create_module_node(name="MODULE_WITH_CLASSES_4", body=CLASS_NODES[:] + (create_node(),)),

    # Functions modules
    create_module_node(body=FUNCTION_NODES[:1]),
    create_module_node(body=(create_node(),) + FUNCTION_NODES[:1]),
    create_module_node(body=FUNCTION_NODES[:3]),
    create_module_node(body=(create_node(),) + FUNCTION_NODES[:3]),
    create_module_node(body=FUNCTION_NODES[:]),
    create_module_node(body=(create_node(),) + FUNCTION_NODES[:]),
    create_module_node(name="MODULE_WITH_FUNCTIONS_1", body=FUNCTION_NODES[:1]),
    create_module_node(name="MODULE_WITH_FUNCTIONS_2", body=FUNCTION_NODES[:1] + (create_node(),)),
    create_module_node(name="MODULE_WITH_FUNCTIONS_3", body=FUNCTION_NODES[:]),
    create_module_node(name="MODULE_WITH_FUNCTIONS_4", body=FUNCTION_NODES[:] + (create_node(),)),

    # Classes and functions modules
    create_module_node(body=CLASS_NODES[:1] + FUNCTION_NODES[:1]),
    create_module_node(body=(create_node(),) + CLASS_NODES[:1] + FUNCTION_NODES[:1]),
    create_module_node(body=FUNCTION_NODES[:3] + CLASS_NODES[:3]),
    create_module_node(body=(create_node(),) + FUNCTION_NODES[:3] + CLASS_NODES[:3]),
    create_module_node(body=FUNCTION_NODES[:] + CLASS_NODES[:]),
    create_module_node(body=(create_node(),) + FUNCTION_NODES[:] + CLASS_NODES[:]),
    create_module_node(name="MODULE_WITH_FUNCTIONS_1", body=FUNCTION_NODES[:1] + CLASS_NODES[:1]),
    create_module_node(name="MODULE_WITH_FUNCTIONS_2", body=FUNCTION_NODES[:1] + CLASS_NODES[:1] + (create_node(),)),
    create_module_node(name="MODULE_WITH_FUNCTIONS_3", body=FUNCTION_NODES[:] + CLASS_NODES[:]),
    create_module_node(name="MODULE_WITH_FUNCTIONS_4", body=FUNCTION_NODES[:] + CLASS_NODES[:1] + (create_node(),)),
)

ALL_NODES = FUNCTION_NODES + CLASS_NODES + MODULE_NODES
