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
    utils,
)
from toolbox.drills import (
    count_toe,
    generate_commit_msg,
    to_reattack,
    pull_repos,
    push_repos,
    update_lines,
    upload_history,
    vpn,
)


@command(name='drills', short_help='drills service related tools')
@argument(
    'group',
    default=utils.generic.get_current_group(),
    callback=utils.generic.is_valid_group)
@option(
    '--name', 'o_name',
    help='Specific name of repository',
    default='all',
    type=str)
@option(
    '--generate-commit-msg', 'o_generate_commit_msg',
    is_flag=True,
    help='Generate drills commit message')
@option(
    '--update-lines', 'o_update_lines', is_flag=True,
    help='Update a group lines.csv with the latest repo info')
@option(
    '--upload-history', 'o_upload_history', is_flag=True,
    help='Show last upload dates on s3 for all groups')
@option(
    '--to-reattack', 'o_to_reattack',
    is_flag=True,
    help='Show findings pending to re-attack and verify')
@option(
    '--pull-repos', 'o_pull_repos',
    is_flag=True,
    help='Pull repos from s3 to fusion for a subs')
@option(
    '--push-repos', 'o_push_repos',
    is_flag=True,
    help='Push repos from fusion to s3 for a subs')
@option(
    '--count-toe', 'o_count_toe', is_flag=True,
    help='Pipelines only, count coverage data and upload it to DynamoDB')
@option(
    '--vpn', 'o_vpn',
    help='Access a subs VPN',
    is_flag=True)
def drills_management(  # pylint: disable=too-many-arguments
    group: str,
    o_name: str,
    o_generate_commit_msg: bool,
    o_update_lines: bool,
    o_upload_history: bool,
    o_to_reattack: bool,
    o_pull_repos: bool,
    o_push_repos: bool,
    o_count_toe: bool,
    o_vpn: bool,
) -> None:
    """Perform operations with the drills service."""
    success: bool = True

    if o_generate_commit_msg:
        success = generate_commit_msg.main(group)
    elif o_update_lines:
        update_lines.main(group)
    elif o_upload_history:
        upload_history.main()
    elif o_to_reattack:
        group = ('all' if group == 'unspecified-subs'
                 else group)
        to_reattack.main(group)
    elif o_pull_repos:
        success = pull_repos.main(group, o_name)
    elif o_push_repos:
        success = push_repos.main(group)
    elif o_count_toe:
        success = count_toe.main(group)
    elif o_vpn and group != 'unspecified-subs':
        success = vpn.main(group)

    sys.exit(0 if success else 1)
