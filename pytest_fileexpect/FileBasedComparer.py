from abc import ABC, abstractmethod
from pathlib import Path

from pytest_fileexpect import ContentNotFoundException



FILENAME_FORMAT = "{}.{}"



class FileBasedComparer(ABC):
    def __init__(self, contentRoot: Path, fileExtension: str):
        self.fileExtension = fileExtension
        self.contentRoot = contentRoot


    def difference(self, contentName, actual):
        if self.fileExtension:
            contentName = FILENAME_FORMAT.format(contentName, self.fileExtension)

        path = self.contentRoot / contentName

        if not (path.exists() and path.is_file()):
            raise ContentNotFoundException(path)

        expected = self.expected(path)

        return self.describeDifference(expected, actual)


    def expected(self, path):
        return self.readContent(path)


    @abstractmethod
    def readContent(self, path): pass


    @abstractmethod
    def describeDifference(self, expected, actual): pass
