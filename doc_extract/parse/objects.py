"""
Includes information containers for
parsed modules, classes, methods/functions
"""
import ast
from doc_extract.generic import DocExtractAbstractClass
from doc_extract.utils import get_python_module_name_from_path


class ParsedObject(DocExtractAbstractClass):
    """
    Abstract parsed parent object
    All Parsed classes should inherit from this class
    """

    def __init__(self, node):
        """
        Stores basic information about the node

        :param node:
        """
        self.node = node
        self.docstring = ast.get_docstring(node)
        self.name = "Unknown type"

    def serialize(self):
        """
        Serializes the parsed object
        returning a dict with its stored information

        :returns: dict
        """
        return {
            "name": self.name,
            "docstring": self.docstring,
        }

    def __str__(self):
        """
        String representation of the instance

        :returns: str
        """
        return "Object: '{name}'".format(name=self.name)

class ParsedModule(ParsedObject):
    """
    ParsedModule information container
    """

    def __init__(self, node, path):
        """
        Stores information about the module
        and calculates its python module path

        :param node:
        :param path:
        """
        super().__init__(node)
        self.name = get_python_module_name_from_path(str(path))
        self.path = path

    def __str__(self):
        """
        String representation of the instance

        :returns: str
        """
        return "Module at <{path}>".format(path=self.path)

class ParsedClass(ParsedObject):
    """
    Class information container
    """

    def __init__(self, node):
        """
        Stores information about the class
        and about its methods

        :param node:
        """
        super().__init__(node)
        self.name = node.name
        self.functions = self.read_functions(node.body)

    def read_functions(self, nodes):
        """
        Filters the nodes for functions and parses them

        :returns: List<ParsedFunction>
        """
        functions = [
            ParsedFunction(node)
            for node in nodes
            if isinstance(node, ast.FunctionDef)
        ]
        return functions

    def serialize(self):
        """
        Serializes the parsed object
        returning a dict with its stored information

        :returns: dict
        """
        base = super().serialize()
        base["methods"] = [ func.serialize() for func in self.functions ]
        return base

    def __str__(self):
        """
        String representation of the instance

        :returns: str
        """
        return "Class: '{name}'".format(name=self.name)

class ParsedFunction(ParsedObject):
    """
    Function information container
    """

    def __init__(self, node):
        """
        Stores information about the function

        :param node:
        """
        super().__init__(node)
        self.name = node.name

    def __str__(self):
        """
        String representation of the instance

        :returns: str
        """
        return "Function: '{name}'".format(name=self.name)
