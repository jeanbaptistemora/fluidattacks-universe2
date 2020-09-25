# Standard library
import textwrap
import pytest

# Local libraries
from toolbox.utils.generic import (
    get_change_request_summary,
    get_change_request_body,
    get_change_request_patch,
    get_change_request_hunks,
    get_change_request_deltas,
)

def test_get_change_request_summary():
    assert 'fix' in get_change_request_summary('45531778')

def test_get_change_request_body():
    expected: str = '- updated config\n'
    assert get_change_request_body('c2848e0b0') == expected

@pytest.mark.skip(reason="Pending to fix")
def test_get_change_request_patch_and_hunks():
    expected: str = textwrap.dedent(
        """
        diff --git a/.gitignore b/.gitignore
        new file mode 100644
        index 000000000..8c388a265
        --- /dev/null
        +++ b/.gitignore
        @@ -0,0 +1,6 @@
        +# Add any directories, files, or patterns you don't want to be tracked by version control
        +**/fusion/*
        +**/reports/*
        +
        +# FLUID concurrent
        +build/
        """[1:])[:-1]

    assert get_change_request_patch('44c9195') == expected
    assert get_change_request_hunks('44c9195') == [expected + '\n']

def test_get_change_request_deltas():
    assert get_change_request_deltas('caf6a78') == 33
