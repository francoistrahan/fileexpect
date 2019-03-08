from pathlib import Path

from .FileBasedComparer import FileBasedComparer



class TextComparer(FileBasedComparer):
    def __init__(self, contentRoot: Path, fileExtension: str = "txt"):
        super().__init__(contentRoot, fileExtension)


    def readContent(self, path):
        raise NotImplemented()


    def describeDifference(self, expected, actual):
        raise NotImplemented()
