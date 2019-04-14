"""
Tests for the exceptions
"""
from doc_extract.exceptions import DocExtractException, ParseError


def test_doc_extract_is_exception():
    """DocExtractException should be subclass of Exception"""
    assert issubclass(DocExtractException, Exception)

def test_parse_error_is_exception():
    """ParseError should be subclass of Exception"""
    assert issubclass(ParseError, Exception)

def test_parse_error_is_doc_extract_exc():
    """ParseError should be subclass of DocExtractException"""
    assert issubclass(ParseError, DocExtractException)
