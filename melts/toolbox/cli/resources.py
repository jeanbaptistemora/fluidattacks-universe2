# Local libraries
import sys

# Third party libraries
from click import (
    argument,
    command,
    option
)

# Local libraries
from toolbox import (
    resources,
    utils
)

SUBS_METAVAR = '[GROUP]'


@command(name='resources', short_help='administrate resources')
@argument(
    'group',
    default=utils.generic.get_current_group(),
    callback=utils.generic.is_valid_group)
@option(
    '--check-repos',
    default=utils.generic.get_current_group(),
    metavar=SUBS_METAVAR)
@option(
    '--clone-from-customer-git',
    'clone',
    is_flag=True,
    help='clone the repositories of a group')
@option(
    '--fingerprint',
    is_flag=True,
    help='get the fingerprint of a group')
@option('--login', is_flag=True, help='login to AWS through OKTA')
@option(
    '--edit-dev', is_flag=True, help='edit the dev secrets of a group')
@option(
    '--read-dev', is_flag=True, help='read the dev secrets of a group')
@option(
    '--edit-prod', is_flag=True, help='edit the prod secrets of a group')
@option(
    '--read-prod', is_flag=True, help='read the prod secrets of a group')
def resources_management(
    group,
    check_repos,
    clone,
    fingerprint,
    login,
    edit_dev,
    read_dev,
    edit_prod,
    read_prod,
):
    """Allows administration tasks within groups"""
    success: bool = True

    if clone:
        success = resources.repo_cloning(group)
    elif fingerprint:
        success = resources.get_fingerprint(group)
    elif edit_dev:
        success = resources.edit_secrets(group, 'dev', f'continuous-{group}')
    elif read_dev:
        success = resources.read_secrets(group, 'dev', f'continuous-{group}')
    elif edit_prod:
        success = resources.edit_secrets(group, 'prod', 'continuous-admin')
    elif read_prod:
        success = resources.read_secrets(group, 'prod', 'continuous-admin')
    elif login:
        success = utils.generic.okta_aws_login(f'continuous-{group}')
    elif check_repos != 'unspecified-subs':
        success = resources.check_repositories(check_repos)

    sys.exit(0 if success else 1)
