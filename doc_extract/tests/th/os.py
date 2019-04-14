"""
Operating system specific code
"""
from os.path import sep


def _get_os_specific_path(path):
    """
    Universalises paths
    for compatibility with different OSs.
    In particular, given a unix-like path
    replaces `/` with `os.path.sep
    """
    return path.replace("/", sep)

def _get_os_specific_paths(*group):
    """
    Universalises a group of paths,
    meaning it calls _get_os_specific_path
    to a collection of strings
    returned the current OS version for those paths
    """
    return tuple(
        _get_os_specific_path(path)
        for path in group
    )
