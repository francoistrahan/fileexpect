from difflib import unified_diff
from pathlib import Path

from .FileBasedComparer import FileBasedComparer



DEFAULT_TXT_EXTENSION = "txt"



class TextComparer(FileBasedComparer):
    def __init__(self, contentRoot: Path, fileExtension: str = DEFAULT_TXT_EXTENSION, updateFiles: bool = None):
        super().__init__(contentRoot, fileExtension, updateFiles)


    def readContent(self, path: Path):
        return path.read_text()


    def writeContent(self, path: Path, content: str):
        path.write_text(content)


    def describeDifference(self, expected, actual):
        if expected == actual:
            return None
        else:
            return "\n".join(unified_diff([expected], [actual], "EXPECTED", "ACTUAL"))
