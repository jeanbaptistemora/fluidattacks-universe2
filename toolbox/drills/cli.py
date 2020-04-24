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
    generate_commit_msg,
    to_reattack,
    pull_repos,
    push_repos,
    update_lines,
    vpn,
)


@command(name='drills', short_help='drills service related tools')
@argument(
    'subscription',
    default=utils.generic.get_current_subscription(),
    callback=utils.generic.is_valid_subscription)
@option(
    '--generate-commit-msg', 'o_generate_commit_msg',
    is_flag=True,
    help='Generate drills commit message')
@option(
    '--update-lines', 'o_update_lines', is_flag=True,
    help='Update a subscription lines.csv with the latest repo info')
@option(
    '--to-reattack', 'o_to_reattack',
    is_flag=True,
    help='Show findings without exploit pending to re-attack and verify')
@option(
    '--to-reattack-exp', 'o_to_reattack_exp',
    is_flag=True,
    help='Show findings with exploit pending to re-attack and verify')
@option(
    '--pull-repos', 'o_pull_repos',
    is_flag=True,
    help='Pull repos from s3 to fusion for a subs')
@option(
    '--push-repos', 'o_push_repos',
    is_flag=True,
    help='Push repos from fusion to s3 for a subs')
@option(
    '--vpn', 'o_vpn',
    help='Access a subs VPN',
    is_flag=True)
def drills_management(
        subscription,
        o_generate_commit_msg,
        o_update_lines,
        o_to_reattack,
        o_to_reattack_exp,
        o_pull_repos,
        o_push_repos,
        o_vpn):
    """Perform operations with the drills service."""
    success: bool = True

    if o_generate_commit_msg:
        success = generate_commit_msg.main(subscription)
    elif o_update_lines:
        update_lines.main(subscription)
    elif o_to_reattack:
        to_reattack.main(False)
    elif o_to_reattack_exp:
        to_reattack.main(True)
    elif o_pull_repos:
        success = pull_repos.main(subscription)
    elif o_push_repos:
        success = push_repos.main(subscription)
    elif o_vpn and subscription != 'unspecified-subs':
        success = vpn.main(subscription)

    sys.exit(0 if success else 1)
