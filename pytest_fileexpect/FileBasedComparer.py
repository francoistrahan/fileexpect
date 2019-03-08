from abc import ABC, abstractmethod
from pathlib import Path

from pytest_fileexpect import ContentNotFoundException



FILENAME_FORMAT = "{}.{}"



class FileBasedComparer(ABC):
    def __init__(self, contentRoot: Path, fileExtension: str):
        self.fileExtension = fileExtension
        self.contentRoot = contentRoot


    def difference(self, contentName, actual):
        path = self.getPathForContent(contentName)

        if not (path.exists() and path.is_file()):
            raise ContentNotFoundException(path)

        expected = self.expected(path)

        return self.describeDifference(expected, actual)


    def getPathForContent(self, contentName):
        if self.fileExtension:
            contentName = FILENAME_FORMAT.format(contentName, self.fileExtension)
        path = self.contentRoot / contentName
        return path


    def expected(self, path):
        return self.readContent(path)


    @abstractmethod
    def readContent(self, path):
        pass  # pragma: no cover


    @abstractmethod
    def describeDifference(self, expected, actual):
        pass  # pragma: no cover
