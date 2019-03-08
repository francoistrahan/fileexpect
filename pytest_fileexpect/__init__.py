__version__ = '0.1.0'



class FileBaseComparerException(Exception): pass



class ContentNotFoundException(FileBaseComparerException):
    def __init__(self, path):
        super().__init__("Expected content file not found: {}".format(path))
