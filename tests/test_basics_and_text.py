from pytest_fileexpect.TextComparer import TextComparer



def test_ctor(shared_datadir):
    tc = TextComparer(shared_datadir)

    assert tc.contentRoot.match("*/data")
    assert "txt" == tc.fileExtension
