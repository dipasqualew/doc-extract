"""
Defines classes that form structures
of the parsed code information
"""
import ast
from doc_extract.generic import DocExtractAbstractClass
from doc_extract.utils import (
    get_python_sources_in_directory,
    get_python_module_name_from_path,
    get_python_name_from_path,
)
from doc_extract.parse.objects import (
    ParsedModule,
    ParsedClass,
    ParsedFunction,
)

class CodeStructure(DocExtractAbstractClass):
    """
    Code structrure abstract class
    """


class LibraryStructure(CodeStructure):
    """
    Code structure of a Python library
    """

    def __init__(self, library_path):
        """
        Stores information about
        the structure of a library

        :param library_path: str - Filepath to the root of the libraty
        """
        self.library_name = get_python_name_from_path(library_path)
        self.library_path = library_path
        self.module_paths = get_python_sources_in_directory(self.library_path)
        self.modules = [
            self.parse_module(module_path)
            for module_path in self.module_paths
        ]

    def parse_module(self, module_path):
        """
        Parsed a module specified via its filepath
        and creates a ModuleStructure out of it

        :param module_path: str
        :returns: ModuleStructure
        """
        with open(module_path) as file_pointer:
            code = ast.parse(file_pointer.read())

        structure = ModuleStructure(module_path)

        for node in ast.walk(code):
            if isinstance(node, ast.Module):
                structure.parse_module(node)
            elif isinstance(node, ast.ClassDef):
                structure.parse_class(node)
            elif isinstance(node, ast.FunctionDef):
                structure.parse_function(node)

        return structure

    def serialize(self):
        """
        Serializes the library information in a dict

        :returns: dict
        """
        return {
            "library_path": self.library_path,
            "modules": [
                module_structure.serialize()
                for module_structure in self.modules
            ]
        }

    def __str__(self):
        """
        String representation of the instance

        :returns: str
        """
        return "Library {name} at {path}".format(
            name=self.library_name,
            path=self.library_path,
        )

class ModuleStructure(CodeStructure):
    """
    Code structure of a Python module
    """

    def __init__(self, module_path):
        """
        Stores information about
        the structure of a module

        :param module_path: str - Filepath of the python module
        """
        self.name = get_python_module_name_from_path(module_path)
        self.path = module_path
        self.module = None
        self.classes = []
        self.functions = []

        self.parsed_references = []

    def parse_module(self, node):
        """
        Parses an ast node creating a ParsedModule object.
        Adds the module to the references

        :param node: ast node
        :returns ParsedModule
        """
        self.module = ParsedModule(node, self.path)
        self.parsed_references.append(node)

    def parse_class(self, node):
        """
        Parses an ast node creating a ParsedClass object.
        Adds the class and its methods to the references

        :param node: ast node
        :returns ParsedModule
        """
        if not node in self.parsed_references:
            parsed_class = ParsedClass(node)
            self.classes.append(parsed_class)
            self.parsed_references.append(node)
            self.parsed_references += [ func.node for func in parsed_class.functions ]

    def parse_function(self, node):
        """
        Parses an ast node creating a ParsedFunction object.
        Adds the function to the references

        :param node: ast node
        :returns ParsedFunction
        """
        if not node in self.parsed_references:
            parsed_function = ParsedFunction(node)
            self.functions.append(parsed_function)
            self.parsed_references.append(node)

    def serialize(self):
        """
        Serializes the library information in a dict

        :returns: dict
        """
        return {
            "module": self.module.serialize(),
            "classes": [ parsed_class.serialize() for parsed_class in self.classes ],
            "functions": [ parsed_function.serialize() for parsed_function in self.functions ],
        }

    def __str__(self):
        """
        String representation of the instance

        :returns: str
        """
        return "Module {name}'s structure".format(
            name=self.name,
        )
