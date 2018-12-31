"""
Shared tests
"""
import ast
import shutil
import tempfile


class TempDirectory(object):
    """
    Creates a tmp directory and populates it with temp files.
    Deletes files and folder on exit
    """

    def __init__(self, dir_suffix="test_tmp_dir", parent_dir=None, file_suffixes=None, keep_open=False):
        """
        Inits the context manager

        :param suffix: str - directory suffix
        :param temp_files_suffixes: list - file suffixes
        """
        if file_suffixes is None:
            file_suffixes = []

        self.parent_dir = parent_dir
        self.dir_suffix = dir_suffix
        self.file_suffixes = file_suffixes
        self.keep_open = keep_open

        self.dir = None
        self.files = []

    def generate_file(self, suffix):
        """
        Generates a temp file.
        Closes the file unless self.keep_open

        :param suffix:
        :returns: str - path to the created temp file
        """
        handler, path = tempfile.mkstemp(suffix=suffix, dir=self.dir)
        if not self.keep_open:
            open(handler).close()
        return path

    def __enter__(self):
        """
        Generates the temp dir and the temp files

        :returns: tuple with self.dir, self.files
        """
        self.dir = tempfile.mkdtemp(suffix=self.dir_suffix, dir=self.parent_dir)
        self.files = list(
            self.generate_file(file_suffix)
            for file_suffix in self.file_suffixes
        )

        return self.dir, self.files

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Deletes the temp files and the temp dir
        """
        shutil.rmtree(self.dir, ignore_errors=True)

def create_node(node_type=None, **kwargs):
    """Creates an ast.Node"""
    if node_type is None:
        node_type = ast.FunctionDef

    name = kwargs.get("name", "function_name")
    body = kwargs.get("body", [])

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
