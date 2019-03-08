from pathlib import Path

from pytest import fixture, raises

from pytest_fileexpect import ContentNotFoundException, detectUpdateInstruction, ENVIRONMENT_UPDATE_KEY, ENVIRONMENT_UPDATE_POSITIVE_WORDS
from pytest_fileexpect.TextComparer import TextComparer



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



def test_ctor_noextension():
    tc = TextComparer(Path("root/does/not/exist"), None)

    assert tc.contentRoot.match("root/does/not/exist")
    assert tc.fileExtension is None
    assert tc.getPathForContent("ze content").match(r"root/does/not/exist/ze content")



def test_fail_on_missing(tc):
    with raises(ContentNotFoundException) as ex:
        tc.difference("missing_content", None)

    assert ex.match(r"Expected content file not found: .*data/missing_content\.txt")



def test_returnNoneOnMatch(tc):
    assert tc.difference("hello_world", "Hello World !!!") is None



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
