from difflib import unified_diff
from pathlib import Path

from .FileBasedComparer import FileBasedComparer



class TextComparer(FileBasedComparer):
    def __init__(self, contentRoot: Path, fileExtension: str = "txt"):
        super().__init__(contentRoot, fileExtension)


    def readContent(self, path: Path):
        return path.read_text()


    def describeDifference(self, expected, actual):
        if expected == actual:
            return None
        else:
            return "\n".join(unified_diff([expected], [actual], "EXPECTED", "ACTUAL"))