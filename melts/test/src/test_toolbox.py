# pylint: disable=unused-argument


from toolbox import (
    utils,
)
from typing import (
    Any,
)

# Constants
SUBS: str = "continuoustest"
SUBS_BAD: str = "not-existing-group"
SUCCESS: int = 0
FAILURE: int = 1
FINDING: str = "720412598"


def test_toolbox_get_group_from_commit_msg(relocate: Any) -> None:
    """Test toolbox.get_group_from_commit_msg."""
    utils.get_commit_subs.main()


def test_toolbox_does_subs_exist(relocate: Any) -> None:
    """Test toolbox.does_subs_exist."""
    assert utils.does_subs_exist.main(SUBS)
    assert not utils.does_subs_exist.main(SUBS_BAD)
