"""
Tests the generic module
module: doc_extract.generic
"""
from doc_extract.tests.mixins import repr_should_be_defined, str_should_be_defined
from doc_extract.generic import DocExtractAbstractClass


def test_doc_extract_abstract_class_repr():
    """The __repr__ method is defined"""
    obj = DocExtractAbstractClass()
    repr_should_be_defined(obj)

def test_doc_extract_abstract_class_str():
    """The __str__ method is defined"""
    obj = DocExtractAbstractClass()
    str_should_be_defined(obj)
