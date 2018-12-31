import ast
from doc_extract.utils import get_python_sources_in_directory
from doc_extract.parse.objects import (
    ParsedModule,
    ParsedClass,
    ParsedFunction,
)


class LibraryStructure(object):

    def __init__(self, library_path):
        self.library_path = library_path
        self.module_paths = get_python_sources_in_directory(self.library_path)
        self.modules = [
            self.parse_module(module_path)
            for module_path in self.module_paths
        ]

    def parse_module(self, module_path):
        with open(module_path) as fp:
            code = ast.parse(fp.read())

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
        return {
            "library_path": self.library_path,
            "modules": [
                module_structure.serialize()
                for module_structure in self.modules
            ]
        }

class ModuleStructure(object):

    def __init__(self, path):
        self.path = path
        self.module = None
        self.classes = []
        self.functions = []

        self.parsed_references = []

    def parse_module(self, node):
        self.module = ParsedModule(node, self.path)
        self.parsed_references.append(node)

    def parse_class(self, node):
        if not node in self.parsed_references:
            parsed_class = ParsedClass(node)
            self.classes.append(parsed_class)
            self.parsed_references.append(node)
            self.parsed_references += [ func.node for func in parsed_class.functions ]

    def parse_function(self, node):
        if not node in self.parsed_references:
            parsed_function = ParsedFunction(node)
            self.functions.append(parsed_function)
            self.parsed_references.append(node)

    def serialize(self):
        return {
            "module": self.module.serialize(),
            "classes": [ parsed_class.serialize() for parsed_class in self.classes ],
            "functions": [ parsed_function.serialize() for parsed_function in self.functions ],
        }
