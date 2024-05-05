class Py2flatException(Exception):
    """
    Base exception for py2flat parser.
    """


class ExceededSize(Py2flatException):
    """
    Maximum size reached.
    """


class RequiredElementMissing(Py2flatException):
    pass


class ElementsNumberIncorrect(Py2flatException):
    """incorrect number of elements."""
