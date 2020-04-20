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
    utils,
)


@command(name='drills', short_help='drills service related tools')
@argument(
    'subscription',
    default=utils.generic.get_current_subscription(),
    callback=utils.generic.is_valid_subscription)
@option(
    '--generate-commit-msg',
    is_flag=True,
    help='Generate drills commit message')
@option(
    '--to-reattack',
    is_flag=True,
    help='Show findings pending to re-attack and verify')
def drills_management(
    subscription,
    generate_commit_msg,
    to_reattack,
):
    """Perform operations with the drills service."""
    success: bool = True

    if generate_commit_msg:
        success = drills.generate_commit_msg.main(subscription)
        sys.exit(0 if success else 1)
    elif to_reattack:
        drills.to_reattack.main()
