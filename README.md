# Intro

This library contains tools to help compare test results against content kept in
content files instead of code.

The library has the following features:

- A base class to implement compare different types of content
- A concrete implementation for text content
- The capacity to update the content files with the current values
- Capacity to defer failing of tests at teardown to allow for updating multiple files
- The capacity to add transformations to content becore comparing (ex: remove random id's before comparing)
- Specialized transformations on text to find and replace a regex
- Control over localisation and naming of content files


# Installation

`pip install fileexpect`

That's it.


# How to Use

The tools can be used with pretty much any test framework (actually, it does not
have to use a framework). Here how you could it with pytest to compare text
content:


## Creating a Fixture

    from pytest import fixture

    @fixture
    def tc():
        rv = TextComparer("path/to/content_folder")
        yield rv
        assert not rv.updatedFiles

Note the line after the `yield` statement. While this line is not necessary, it
will make you tests fail if it has updated an expected content file. The reason
why it is done after the test instead of directly uppon update is to allow a
single test to go and update multiple files.


## Using the Fixture Inside of a Test

    def test_something(tc):
        result = bigreport()
        diff = tc.differences("command_output", result)
        assert diff is None

If the value of `result` is the same as the content of
`path/to/content_folder/command_output.txt`, `differences` will return `None`
and the test will pass. If the contents differ, `diff` will contain a familiar
representation of the differences between the expected vs actual content.

If your IDE does not show you the diff, you may want to store it in a variable
before checking and print it; pytest has a nice way of handling this when run
from the command line.

If the file `path/to/content_folder/command_output.txt` does not exist,
`differences` will throw a `ContentNotFoundException`.


## Creating or Updating the Content of Content Files.

The best way to update content files is to run your tests with the environment
variable UPDATE_EXPECTED_FILES set to any of the following: "yes", "y", "true",
"t" or "1".

Alternatively, you may explicitely pass `updateFiles=True` to the constructor
when creating your comparer.

In both cases, instead of comparing the content, it would save the content of
the variable `result` in the content file. You would then probably want to
review the file and, if good, commit it to your CVS.

Re-running the test without the environment or explicit flag would now compare
with the new content.


## More details

Given that these tools are meant to be used within unit tests, the best way to
learn a bit more about it is to go and look at the unit tests of the library
itself.

The only thing you will not see there is the bit about failing tests after
update, as I insist on full coverage and all green tests.
