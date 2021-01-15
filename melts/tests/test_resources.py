# pylint: disable=unused-argument
# Standard library
import os
from typing import Any

# Third parties imports

# Local libraries
from toolbox import resources

# Constants
SUBS: str = 'continuoustest'
SUBS_BAD: str = 'not-existing-group'
SUCCESS: int = 0
FAILURE: int = 1
FINDING: str = '720412598'
EMAIL: str = 'dalvarez@fluidattacks.com'


def test_toolbox_get_fingerprint(relocate: Any) -> None:
    """Run required toolbox commands."""
    assert resources.get_fingerprint(SUBS)
    assert not resources.get_fingerprint(SUBS_BAD)
    os.mkdir(os.path.join('groups', "testfinger"))
    assert not resources.get_fingerprint('testfinger')
    os.mkdir(os.path.join('groups/testfinger', "fusion"))
    assert not resources.get_fingerprint('testfinger')
    os.rmdir(os.path.join('groups/testfinger', "fusion"))
    os.rmdir(os.path.join('groups', "testfinger"))
