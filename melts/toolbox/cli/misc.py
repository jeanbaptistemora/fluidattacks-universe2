# Local libraries
import sys

# Third party libraries
from click import (
    argument,
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
@argument(
    'group',
    default=utils.generic.get_current_group(),
    callback=utils.generic.is_valid_group)
@option('--check-commit-msg', is_flag=True, help='validate commit msg syntax')
@option('--is-drills-commit', is_flag=True)
@option('--has-forces', is_flag=True)
def misc_management(
        group,
        check_commit_msg,
        is_drills_commit,
        has_forces,
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
    elif has_forces:
        sys.exit(0 if utils.integrates.has_forces(group) else 1)
