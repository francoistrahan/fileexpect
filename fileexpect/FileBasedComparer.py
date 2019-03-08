from abc import ABC, abstractmethod
from pathlib import Path

from . import ContentNotFoundException, detectUpdateInstruction



FILENAME_FORMAT = "{}.{}"



class FileBasedComparer(ABC):
    def __init__(self, contentRoot: Path, fileExtension: str, updateFiles: bool = None):
        if isinstance(contentRoot, str):
            contentRoot = Path(contentRoot)

        self.updatedFiles = []

        self.fileExtension = fileExtension
        self.contentRoot = contentRoot

        if updateFiles is None:
            updateFiles = detectUpdateInstruction()

        self.updateFiles = updateFiles
        self.transforms = []


    def difference(self, contentName, actual):
        path = self.getPathForContent(contentName)

        if self.updateFiles:
            self.writeContent(path, actual)
            self.updatedFiles.append(path)

            return None
        else:
            if not (path.exists() and path.is_file()):
                raise ContentNotFoundException(path)

            expected = self.expected(path)

            for t in self.transforms:
                expected = t(expected)
                actual = t(actual)

            return self.describeDifference(expected, actual)


    def getPathForContent(self, contentName):
        if self.fileExtension:
            contentName = FILENAME_FORMAT.format(contentName, self.fileExtension)
        path = self.contentRoot / contentName
        return path


    def expected(self, path):
        return self.readContent(path)


    def addTransform(self, transform):
        self.transforms.append(transform)


    @abstractmethod
    def readContent(self, path):
        pass  # pragma: no cover


    @abstractmethod
    def writeContent(self, path, content):
        pass  # pragma: no cover


    @abstractmethod
    def describeDifference(self, expected, actual):
        pass  # pragma: no cover
