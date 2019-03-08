from pathlib import Path

from pytest import fixture, raises

from pytest_fileexpect import ContentNotFoundException, detectUpdateInstruction, ENVIRONMENT_UPDATE_KEY, ENVIRONMENT_UPDATE_POSITIVE_WORDS
from pytest_fileexpect.FileBasedComparer import FILENAME_FORMAT
from pytest_fileexpect.TextComparer import DEFAULT_TXT_EXTENSION, TextComparer



HELLO_WORLD_CONTENT_NAME = "hello_world"

SAMPLE_THREE_LINE_CONTENT = "Here is a nice\n" \
                            "three line\n" \
                            "file with a trailing return\n"



@fixture
def tc(shared_datadir):
    return TextComparer(shared_datadir)



@fixture
def env_update(monkeypatch):
    return monkeypatch.setenv(ENVIRONMENT_UPDATE_KEY, ENVIRONMENT_UPDATE_POSITIVE_WORDS[0])



def test_detectUpdateInstruction_noUpdate():
    assert not detectUpdateInstruction()



def test_detectUpdateInstruction_EnvUpdate(env_update):
    assert detectUpdateInstruction()



def test_ctor():
    tc = TextComparer(Path("root/does/not/exist"))

    assert tc.contentRoot.match("root/does/not/exist")
    assert "txt" == tc.fileExtension
    assert tc.getPathForContent("ze content").match("root/does/not/exist/ze content.txt")
    assert tc.updateFiles == False



def test_ctor_noExtension():
    tc = TextComparer(Path("root/does/not/exist"), None)

    assert tc.contentRoot.match("root/does/not/exist")
    assert tc.fileExtension is None
    assert tc.getPathForContent("ze content").match(r"root/does/not/exist/ze content")



def test_ctor_forceUpdate():
    tc = TextComparer(Path("root/does/not/exist"), updateFiles=True)

    assert tc.updateFiles == True



def test_fail_on_missing(tc):
    with raises(ContentNotFoundException) as ex:
        tc.difference("missing_content", None)

    assert ex.match(r"Expected content file not found: .*data/missing_content\.txt")



def test_returnNoneOnMatch(tc):
    assert tc.difference(HELLO_WORLD_CONTENT_NAME, "Hello World !!!") is None



def test_describeTextMismatch(tc):
    EXPECTED = ("--- EXPECTED\n"
                "\n"
                "+++ ACTUAL\n"
                "\n"
                "@@ -1 +1 @@\n"
                "\n"
                "-Hello World !!!\n"
                "+Bonjour le monde !!!")

    diff = tc.difference("hello_world", "Bonjour le monde !!!")
    print(diff)
    assert EXPECTED == diff



def test_updateMissing(env_update, tc):
    CONTENT_NAME = "missing_at_first"
    CONTENT = SAMPLE_THREE_LINE_CONTENT

    root = tc.contentRoot
    contentPath = root / FILENAME_FORMAT.format(CONTENT_NAME, DEFAULT_TXT_EXTENSION)
    print("Content path:", contentPath)

    assert tc.difference(CONTENT_NAME, CONTENT) is None

    assert contentPath.exists() and contentPath.is_file()

    assert CONTENT == contentPath.read_text()



def test_updateExisting(env_update, tc):
    contentName = HELLO_WORLD_CONTENT_NAME
    content = SAMPLE_THREE_LINE_CONTENT

    root = tc.contentRoot
    contentPath = root / FILENAME_FORMAT.format(contentName, DEFAULT_TXT_EXTENSION)

    print("Content path:", contentPath)

    assert tc.difference(contentName, content) is None

    assert contentPath.exists() and contentPath.is_file()

    assert content == contentPath.read_text()
