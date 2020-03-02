# Standard library
import sys
import shlex

# Third parties libraries
import pytest
import unittest.mock

# Local libraries
from toolbox import cli

def test_toolbox_main(relocate):
    """Test toolbox.main."""
    with pytest.raises(SystemExit) as exc:
        cli.main()
    assert exc.value.code

    with pytest.raises(SystemExit) as exc:
        with unittest.mock.patch.object(
                sys, 'argv', shlex.split('toolbox --subs test')):
            cli.main()
    assert exc.value.code
