# Standard libraries
import sys

# Third party libraries
from click import (
    argument,
    command,
    option,
    echo,
)

# Local libraries
from toolbox.utils import (
    generic,
    vpn,
    does_subs_exist,
    get_commit_subs,
)


@command(name='utils', short_help='Generic utilities')
@argument(
    'subscription',
    default=generic.get_current_subscription(),
    callback=generic.is_valid_subscription)
@option(
    '--does-subs-exist', 'o_does_subs_exist',
    help='Check if a subscription exists.',
    is_flag=True)
@option(
    '--get-commit-subs', 'o_get_commit_subs',
    help='get the subscription name from the commmit msg.',
    is_flag=True)
@option(
    '--vpn', 'o_vpn',
    help='Access a subs VPN',
    is_flag=True)
def utils_management(
        subscription,
        o_does_subs_exist,
        o_get_commit_subs,
        o_vpn):
    if o_vpn and subscription != 'unspecified-subs':
        sys.exit(0 if vpn.main(subscription) else 1)
    elif o_does_subs_exist:
        sys.exit(0 if does_subs_exist.main(subscription) else 1)
    elif o_get_commit_subs:
        subs = get_commit_subs.main()
        echo(subs)
        sys.exit(0 if subs else 1)
