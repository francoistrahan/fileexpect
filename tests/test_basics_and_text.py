from pathlib import Path

from pytest import fixture, raises

from fileexpect import ContentNotFoundException, detectUpdateInstruction, ENVIRONMENT_UPDATE_KEY, ENVIRONMENT_UPDATE_POSITIVE_WORDS
from fileexpect.FileBasedComparer import FILENAME_FORMAT
from fileexpect.TextComparer import DEFAULT_TXT_EXTENSION, TextComparer



HELLO_WORLD_CONTENT_NAME = "hello_world"

SAMPLE_THREE_LINE_CONTENT = "Here is a nice\n" \
                            "three line\n" \
                            "file with a trailing return\n"

REGEX_REMOVE_IDS = """id=[0-9]{5}"""
REGEX_REMOVE_CLASSES = '''class="[0-9]{5}"'''



@fixture
def tc(shared_datadir):
    rv = TextComparer(shared_datadir)
    rv.addRegexReplace(REGEX_REMOVE_IDS, "id=[REMOVED_ID]")
    rv.addRegexReplace(REGEX_REMOVE_CLASSES, "id=[REMOVED_CLASS]")
    yield rv
    # You would probably want to assert not rv.updatedFiles



@fixture
def env_update(monkeypatch):
    return monkeypatch.setenv(ENVIRONMENT_UPDATE_KEY, ENVIRONMENT_UPDATE_POSITIVE_WORDS[0])



def test_detectUpdateInstruction_noUpdate():
    assert not detectUpdateInstruction()



def test_detectUpdateInstruction_EnvUpdate(env_update):
    assert detectUpdateInstruction()



def test_ctor():
    tc = TextComparer("root/does/not/exist")

    assert tc.contentRoot.match("root/does/not/exist")
    assert "txt" == tc.fileExtension
    assert tc.getPathForContent("ze content").match("root/does/not/exist/ze content.txt")
    assert tc.updateFiles == False
    assert tc.updatedFiles == []
    assert tc.transforms == []



def test_ctor_noExtension():
    tc = TextComparer("root/does/not/exist", None)

    assert tc.fileExtension is None
    assert tc.getPathForContent("ze content").match(r"root/does/not/exist/ze content")



def test_ctor_forceUpdate():
    tc = TextComparer(Path("root/does/not/exist"), updateFiles=True)

    assert tc.updateFiles == True



def test_fail_on_missing(tc):
    with raises(ContentNotFoundException) as ex:
        tc.difference("missing_content", None)

    assert ex.match(r"Expected content file not found: .*data/missing_content\.txt")
    assert tc.updatedFiles == []



def test_returnNoneOnMatch(tc):
    assert tc.difference(HELLO_WORLD_CONTENT_NAME, "Hello World !!!") is None
    assert tc.updatedFiles == []



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
    assert tc.updatedFiles == []



def test_updateMissing(env_update, tc):
    CONTENT_NAME = "missing_at_first"
    CONTENT = SAMPLE_THREE_LINE_CONTENT

    root = tc.contentRoot
    contentPath = root / FILENAME_FORMAT.format(CONTENT_NAME, DEFAULT_TXT_EXTENSION)
    print("Content path:", contentPath)

    assert tc.difference(CONTENT_NAME, CONTENT) is None

    assert contentPath.exists() and contentPath.is_file()

    assert CONTENT == contentPath.read_text()
    assert tc.updatedFiles == [contentPath]



def test_updateExisting(env_update, tc):
    contentName = HELLO_WORLD_CONTENT_NAME
    content = SAMPLE_THREE_LINE_CONTENT

    root = tc.contentRoot
    contentPath = root / FILENAME_FORMAT.format(contentName, DEFAULT_TXT_EXTENSION)

    print("Content path:", contentPath)

    assert tc.difference(contentName, content) is None

    assert contentPath.exists() and contentPath.is_file()

    assert content == contentPath.read_text()
    assert tc.updatedFiles == [contentPath]



def test_regex_transform(tc):
    NAME = "file_with_random_elements"
    CONTENT = ("This is a simple document that contains a few pieces of random data. Because of\n"
               "this, it is not possible to test with exact string matching.\n"
               "\n"
               "The transform will be used to take the randomness out of both the original and\n"
               "expected document.\n"
               "\n"
               "This line won't clash: id=54321\n"
               "This line won't either: class=\"65432\"\n"
               "This one will, but not on the id: id=76543, CHANGED\n"
               "This one will, but not on the class: class=\"87654\", CHANGED\n"
               "\n"
               "Voilà !\n")

    EXPECTED_DIFF = ("--- EXPECTED\n"
                     "\n"
                     "+++ ACTUAL\n"
                     "\n"
                     "@@ -6,7 +6,7 @@\n"
                     "\n"
                     " \n"
                     " This line won't clash: id=[REMOVED_ID]\n"
                     " This line won't either: id=[REMOVED_CLASS]\n"
                     "-This one will, but not on the id: id=[REMOVED_ID], CHANGE_ME\n"
                     "-This one will, but not on the class: id=[REMOVED_CLASS], CHANGE_ME\n"
                     "+This one will, but not on the id: id=[REMOVED_ID], CHANGED\n"
                     "+This one will, but not on the class: id=[REMOVED_CLASS], CHANGED\n"
                     " \n"
                     " Voilà !")

    diff = tc.difference(NAME, CONTENT)
    print(diff)

    assert EXPECTED_DIFF == diff
