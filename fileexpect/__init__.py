from os import environ



ENVIRONMENT_UPDATE_KEY = "UPDATE_EXPECTED_FILES"
ENVIRONMENT_UPDATE_POSITIVE_WORDS = ("yes", "y", "true", "t", "1")



class FileBaseComparerException(Exception): pass



class ContentNotFoundException(FileBaseComparerException):
    def __init__(self, path):
        super().__init__("Expected content file not found: {}".format(path))



def detectUpdateInstruction():
    # Check if environment asks for it
    fromEnv = environ.get(ENVIRONMENT_UPDATE_KEY, "no")
    fromEnv = fromEnv.lower()

    if fromEnv in ENVIRONMENT_UPDATE_POSITIVE_WORDS:
        return True

    return False
