# Local libraries
import sys

# Third party libraries
from click import (
    command,
    option,
)

# Local libraries
from toolbox import (
    drills,
    forces,
    generic,
    utils,
)


def do_check_commit_msg() -> bool:
    summary: str = utils.generic.get_change_request_summary()
    body: str = utils.generic.get_change_request_body()
    success: bool = False

    if drills.commit.is_drills_commit(summary):
        success = drills.commit.is_valid_summary(summary)
    elif forces.commit.is_exploits_commit(summary):
        success = forces.commit.is_valid_summary(summary)
    else:
        success = generic.commit.is_valid_summary(summary) \
            and generic.commit.has_short_line_length(summary, body)
    return success


@command(name='misc', short_help='miscellaneous checks')
@option('--check-commit-msg', is_flag=True, help='validate commit msg syntax')
@option('--is-drills-commit', is_flag=True)
@option('--is-exploits-commit', is_flag=True)
def misc_management(
    check_commit_msg,
    is_drills_commit,
    is_exploits_commit,
):
    success: bool

    if is_drills_commit:
        summary: str = utils.generic.get_change_request_summary()
        success = drills.commit.is_drills_commit(summary)
        sys.exit(0 if success else 1)

    elif check_commit_msg:
        success = do_check_commit_msg()
        sys.exit(0 if success else 1)

    elif is_exploits_commit:
        summary: str = utils.generic.get_change_request_summary()
        success = forces.commit.is_exploits_commit(summary)
        sys.exit(0 if success else 1)
