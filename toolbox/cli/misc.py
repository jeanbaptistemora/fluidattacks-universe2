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
    logger,
    utils,
)


def do_check_commit_msg() -> bool:
    summary: str = utils.get_commit_summary()
    success: bool = False

    if drills.commit.is_drills_commit(summary):
        success = drills.commit.is_valid_msg(summary)
    elif forces.commit.is_exploits_commit(summary):
        success = forces.commit.is_valid_msg(summary)
    else:
        logger.error('Your commit does not fit into any category')
        success = False
    return success


@command(name='misc', short_help='miscellaneous checks')
@option('--check-commit-msg', is_flag=True, help='validate commit msg syntax')
def misc_management(
    check_commit_msg,
):
    if check_commit_msg:
        success: bool = do_check_commit_msg()
        sys.exit(0 if success else 1)
