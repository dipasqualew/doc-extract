"""
Tests for CodeStructure
module: doc_extract.parse.structures
"""
from doc_extract.generic import DocExtractAbstractClass
from doc_extract.parse.structures import CodeStructure


def test_is_subclass():
    """Is it instance of DocExtractAbstractClass"""
    assert issubclass(CodeStructure, DocExtractAbstractClass)
