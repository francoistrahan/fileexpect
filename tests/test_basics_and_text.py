from pytest import fixture, raises

from pytest_fileexpect import ContentNotFoundException
from pytest_fileexpect.TextComparer import TextComparer



@fixture
def tc(shared_datadir):
    return TextComparer(shared_datadir)



def test_ctor(tc):
    assert tc.contentRoot.match("*/data")
    assert "txt" == tc.fileExtension



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
