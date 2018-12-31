import ast
from doc_extract.utils import get_python_module_name_form_path


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
        self.name = get_python_module_name_form_path(str(path))
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
