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
    '--to-reattack', 'o_to_reattack',
    is_flag=True,
    help='Show findings pending to re-attack and verify')
@option(
    '--vpn', 'o_vpn',
    help='Access a subs VPN',
    is_flag=True)
def drills_management(
        subscription,
        o_generate_commit_msg,
        o_to_reattack,
        o_vpn):
    """Perform operations with the drills service."""
    if o_generate_commit_msg:
        sys.exit(0 if generate_commit_msg.main(subscription) else 1)
    elif o_to_reattack:
        to_reattack.main()
    elif o_vpn and subscription != 'unspecified-subs':
        sys.exit(0 if vpn.main(subscription) else 1)
