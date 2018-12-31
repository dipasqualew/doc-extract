"""
Generic definitions for the library
"""

class DocExtractAbstractClass(object):
    """
    Generic root abstract class
    of the doc_extract library
    """

    def __str__(self):
        """
        String representation of the instance

        :returns: str
        """
        return self.__class__.__name__

    def __repr__(self):
        """
        Canonical string representation of the instance

        :returns: str
        """
        return "<{self}>".format(self=self)
