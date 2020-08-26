# Standard library
import os
import re
import sys

# Third parties imports
import pytest

# Local libraries
from toolbox import resources

# Constants
SUBS: str = 'continuoustest'
SUBS_BAD: str = 'not-existing-group'
SUCCESS: int = 0
FAILURE: int = 1
FINDING: str = '720412598'
EMAIL: str = 'dalvarez@fluidattacks.com'


def test_toolbox_get_fingerprint(relocate):
    """Run required toolbox commands."""
    assert resources.get_fingerprint(SUBS)
    assert not resources.get_fingerprint(SUBS_BAD)
    os.mkdir(os.path.join('groups', "testfinger"))
    assert not resources.get_fingerprint('testfinger')
    os.mkdir(os.path.join('groups/testfinger', "fusion"))
    assert not resources.get_fingerprint('testfinger')
    os.rmdir(os.path.join('groups/testfinger', "fusion"))
    os.rmdir(os.path.join('groups', "testfinger"))


def test_toolbox_check_repositories(relocate):
    """Run required toolbox commands."""
    assert resources.check_repositories(SUBS)
    assert not resources.check_repositories(SUBS_BAD)
