from abc import ABC
from pathlib import Path



FILENAME_FORMAT = "{}.{}"



class FileBasedComparer(ABC):
    def __init__(self, contentRoot: Path, fileExtension: str):
        self.fileExtension = fileExtension
        self.contentRoot = contentRoot


    def differences(self, contentName, actual):
        if self.fileExtension:
            contentName = FILENAME_FORMAT.format(contentName, self.fileExtension)

        path = self.contentRoot / contentName

        assert path.exists() and path.is_file()

        expected = self.readContent(path)

        return self.areEqual(expected, actual)


    def readContent(self, path): pass


    def areEqual(self, expected, actual): pass
