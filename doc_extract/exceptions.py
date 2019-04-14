"""
Exceptions module
"""

class DocExtractException(Exception):
    """
    Base exception class for
    all the doc_extract exceptions
    to be exposed as a "catch-all"
    for library consumers
    """


class ParseError(DocExtractException):
    """
    Raised on parse error
    """
