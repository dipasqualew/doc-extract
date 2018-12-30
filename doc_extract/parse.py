import ast
from pathlib import Path

class ParsedObject(object):
    def __init__(self, node):
        self.node = node
        self.docstring = ast.get_docstring(node)
        self.name = "Unknown object"

    def serialize(self):
        return {
            "name": self.name,
            "docstring": self.docstring,
        }

class ParsedModule(ParsedObject):
    def __init__(self, node, path):
        super().__init__(node)
        self.name = "Module"
        self.path = path

    def __str__(self):
        return "Module at <{path}>".format(path=self.path)

class ParsedClass(ParsedObject):
    def __init__(self, node):
        super().__init__(node)
        self.name = node.name
        self.functions = self.read_functions(node.body)

    def read_functions(self, nodes):
        functions = [
            ParsedFunction(node)
            for node in nodes
            if isinstance(node, ast.FunctionDef)
        ]
        return functions

    def serialize(self):
        base = super().serialize()
        base["methods"] = [ func.serialize() for func in self.functions ]
        return base

    def __str__(self):
        return "Class {name}".format(name=self.name)

class ParsedFunction(ParsedObject):
    def __init__(self, node):
        super().__init__(node)
        self.name = node.name

    def __str__(self):
        return "Function {name}".format(name=self.name)

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

class LibraryStructure(object):

    def __init__(self, library_path):
        self.library_path = library_path
        self.module_paths = get_python_sources_in_directory(self.library_path)
        self.modules = [
            self.parse_module(module_path)
            for module_path in self.module_paths
        ]

    def parse_module(self, module_path):
        module_structure = analyse_module_path(module_path)
        return module_structure

    def serialize(self):
        return {
            "library_path": self.library_path,
            "modules": [
                module_structure.serialize()
                for module_structure in self.modules
            ]
        }

def get_python_sources_in_directory(directory):
    result = list(Path(directory).rglob("*.py"))
    return result


def analyse_module_path(module_path):
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
