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
    generic,
    utils,
)


def do_check_commit_msg() -> bool:
    summary: str = utils.generic.get_change_request_summary()
    body: str = utils.generic.get_change_request_body()
    success: bool = False

    if drills.commit.is_drills_commit(summary):
        success = drills.commit.is_valid_summary(summary, body)
    else:
        success = generic.commit.is_valid_summary(summary) \
            and generic.commit.has_short_line_length(summary, body) \
            and generic.commit.is_under_100_deltas() \

    return success


@command(name='misc', short_help='miscellaneous checks')
@option('--check-commit-msg', is_flag=True, help='validate commit msg syntax')
@option('--is-drills-commit', is_flag=True)
def misc_management(
        check_commit_msg,
        is_drills_commit,
):
    success: bool

    if is_drills_commit:
        summary: str = utils.generic.get_change_request_summary()
        success = drills.commit.is_drills_commit(summary)
        sys.exit(0 if success else 1)

    elif check_commit_msg:
        success_message = do_check_commit_msg()
        success_content = drills.lint.check_folder_content()
        sys.exit(0 if success_message and success_content else 1)
