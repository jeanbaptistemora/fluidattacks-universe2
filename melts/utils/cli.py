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
    does_subs_exist,
    get_commit_subs,
)


@command(name='utils', short_help='Generic utilities')
@argument(
    'group',
    default=generic.get_current_group(),
    callback=generic.is_valid_group)
@option(
    '--does-subs-exist', 'o_does_subs_exist',
    help='Check if a group exists.',
    is_flag=True)
@option(
    '--get-commit-subs', 'o_get_commit_subs',
    help='get the group name from the commmit msg.',
    is_flag=True)
def utils_management(
        group,
        o_does_subs_exist,
        o_get_commit_subs):
    if o_does_subs_exist:
        sys.exit(0 if does_subs_exist.main(group) else 1)
    elif o_get_commit_subs:
        subs = get_commit_subs.main()
        echo(subs)
        sys.exit(0 if subs else 1)
