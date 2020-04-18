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
    default=utils.get_current_subscription(),
    callback=utils.is_valid_subscription)
@option(
    '--generate-commit-msg',
    is_flag=True,
    help='Generate drills commit message')
@option(
    '--findings-pending-to-verify',
    is_flag=True,
    help='Show findings pending to verify')
def drills_management(
    subscription,
    generate_commit_msg,
    findings_pending_to_verify,
):
    """Perform operations with the drills service."""
    success: bool = True

    if generate_commit_msg:
        success = drills.generate_commit_msg.main(subscription)
        sys.exit(0 if success else 1)
    elif findings_pending_to_verify:
        drills.findings_pending_to_verify.main()
