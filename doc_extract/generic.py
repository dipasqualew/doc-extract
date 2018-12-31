"""
Generic definitions for the library
"""

class DocExtractAbstractClass(object):
    """
    Generic root abstract class
    of the doc_extract library
    """

    def __repr__(self):
        """
        Representation of the instance

        :returns: str
        """
        return "<{self}>".format(self=self)
