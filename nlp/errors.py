

class BaseEsception(Exception):

    pass


class MatrixFileDoesNotExist(BaseEsception):
    """Raised when a matrix file does not exist."""
    pass
