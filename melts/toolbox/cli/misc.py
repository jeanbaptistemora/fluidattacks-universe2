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
    callback=utils.generic.is_valid_group,
)
@option('--check-commit-msg', is_flag=True, help='validate commit msg syntax')
@option('--is-drills-commit', is_flag=True)
@option('--filter-groups-with-forces')
@option('--get-group-language', is_flag=True)
@option('--has-drills', is_flag=True)
def misc_management(
    group: str,
    check_commit_msg: bool,
    is_drills_commit: bool,
    filter_groups_with_forces: str,
    get_group_language: bool,
    has_drills: bool,
) -> None:
    success: bool = False

    if is_drills_commit:
        summary: str = utils.generic.get_change_request_summary()
        success = drills.commit.is_drills_commit(summary)

    elif check_commit_msg:
        success_message = do_check_commit_msg()
        success_content = drills.lint.check_folder_content()
        success = success_message and success_content

    elif filter_groups_with_forces:
        success = utils.integrates.filter_groups_with_forces_as_json_str(tuple(
            filter_groups_with_forces.split(' '),
        ))
    elif get_group_language:
        print(utils.integrates.get_group_language(group))
        success = True
    elif has_drills:
        success = utils.integrates.has_drills(group)

    sys.exit(0 if success else 1)
