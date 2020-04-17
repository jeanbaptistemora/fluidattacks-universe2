# Local libraries
from toolbox import (
    drills
)


def test_drills_is_valid_commit_msg(relocate):
    """Test toolbox.is_drills_commit."""
    drills.is_valid_commit_msg.main()
