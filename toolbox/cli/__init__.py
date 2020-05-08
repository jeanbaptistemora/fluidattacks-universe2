# pylint: disable=unused-argument
# pylint: disable=import-outside-toplevel

# Standard library
import functools
import sys

# Third parties imports
import click

# Local libraries
from toolbox import (
    resources,
    toolbox,
    analytics,
    forces,
    sorts,
    utils,
    drills,
)
from .misc import misc_management


EXP_METAVAR = '[<EXPLOIT | all>]'
SUBS_METAVAR = '[GROUP]'


def _valid_integrates_token(ctx, param, value):
    from toolbox import constants
    assert constants


def _convert_exploit(ctx, param, value):
    return '' if value == 'all' else value


@click.group(name='entrypoint')
def entrypoint():
    """Main comand line group."""


@click.command(name='resources', short_help='administrate resources')
@click.argument(
    'group',
    default=utils.generic.get_current_group(),
    callback=utils.generic.is_valid_group)
@click.option(
    '--check-repos',
    default=utils.generic.get_current_group(),
    metavar=SUBS_METAVAR)
@click.option(
    '--clone-from-customer-git',
    'clone',
    is_flag=True,
    help='clone the repositories of a group')
@click.option(
    '--fingerprint',
    is_flag=True,
    help='get the fingerprint of a group')
@click.option('--login', is_flag=True, help='login to AWS through OKTA')
@click.option(
    '--mailmap',
    '-mp',
    is_flag=True,
    help='check if the mailmap of a group is valid')
@click.option(
    '--edit-dev', is_flag=True, help='edit the dev secrets of a group')
@click.option(
    '--read-dev', is_flag=True, help='read the dev secrets of a group')
@click.option(
    '--edit-prod', is_flag=True, help='edit the prod secrets of a group')
@click.option(
    '--read-prod', is_flag=True, help='read the prod secrets of a group')
def resources_management(
    group,
    check_repos,
    clone,
    fingerprint,
    mailmap,
    login,
    edit_dev,
    read_dev,
    edit_prod,
    read_prod,
):
    """Allows administration tasks within groups"""
    success: bool = True

    if mailmap:
        success = resources.check_mailmap(group)
    elif clone:
        success = resources.repo_cloning(group)
    elif fingerprint:
        success = resources.get_fingerprint(group)
    elif edit_dev:
        success = resources.edit_secrets(group, 'dev', f'continuous-{group}')
    elif read_dev:
        success = resources.read_secrets(group, 'dev', f'continuous-{group}')
    elif edit_prod:
        success = resources.edit_secrets(group, 'prod', f'continuous-admin')
    elif read_prod:
        success = resources.read_secrets(group, 'prod', f'continuous-admin')
    elif login:
        success = utils.generic.okta_aws_login(f'continuous-{group}')
    elif check_repos != 'unspecified-subs':
        success = resources.check_repositories(check_repos)

    sys.exit(0 if success else 1)


@click.command(name='forces', short_help='use the exploits')
@click.argument(
    'group',
    default=utils.generic.get_current_group(),
    callback=utils.generic.is_valid_group)
@click.option(
    '--check-sync',
    '--sync',
    metavar=EXP_METAVAR,
    help='check if exploits results are the same as on Integrates',
    callback=_convert_exploit)
@click.option(
    '--decrypt', is_flag=True, help='decrypt the secrets of a group')
@click.option(
    '--encrypt', is_flag=True, help='encrypt the secrets of a group')
@click.option('--fill-with-iexps', is_flag=True)
@click.option('--generate-exploits', is_flag=True)
@click.option('--get-vulns', type=click.Choice(['dynamic', 'static', 'all']))
@click.option(
    '--lint-exps',
    metavar=EXP_METAVAR,
    help='lint exploits for a group',
    callback=_convert_exploit)
@click.option('--lint-changed-exploits', is_flag=True)
@click.option('--run-exps', '--run', '-r', is_flag=True, help='run exploits')
@click.option(
    '--static',
    '-s',
    metavar=EXP_METAVAR,
    help='run a static exploit',
    callback=_convert_exploit)
@click.option(
    '--dynamic',
    '-d',
    metavar=EXP_METAVAR,
    help='run a dynamic exploit',
    callback=_convert_exploit)
@click.option('--upload-exps-from-repo-to-integrates', is_flag=True)
def forces_management(
    group,
    check_sync,
    decrypt,
    encrypt,
    fill_with_iexps,
    get_vulns,
    generate_exploits,
    lint_exps,
    lint_changed_exploits,
    run_exps,
    static,
    dynamic,
    upload_exps_from_repo_to_integrates,
):
    """Perform operations with the forces service."""
    success: str = True
    filter_str: str = ''

    if not toolbox.has_forces(group):
        raise click.BadArgumentUsage(
            f'{group} group has no forces')

    if run_exps:
        if dynamic is not None:
            success = toolbox.run_dynamic_exploits(group, dynamic)
        elif static is not None:
            success = toolbox.run_static_exploits(group, static)

    elif check_sync is not None:
        success = forces.sync.are_exploits_synced(group, check_sync)

    elif fill_with_iexps:
        filter_str = group or '*'
        toolbox.fill_with_iexps(subs_glob=filter_str, create_files=True)

    elif generate_exploits:
        filter_str = group or '*'
        toolbox.generate_exploits(subs_glob=filter_str)

    elif get_vulns:
        success = toolbox.get_vulnerabilities_yaml(group, get_vulns)

    elif lint_exps is not None:
        filter_str = lint_exps
        success = forces.lint.many_exploits_by_subs_and_filter(
            group, lint_exps)

    elif lint_changed_exploits:
        success = forces.lint.many_exploits_by_change_request()

    elif decrypt:
        success = forces.secrets.decrypt(group)

    elif encrypt:
        success = forces.secrets.encrypt(group)

    elif upload_exps_from_repo_to_integrates:
        success = forces.upload.from_repo_to_integrates(group)

    sys.exit(0 if success else 1)


@click.command(name='integrates', short_help='use the integrates API')
@click.argument(
    'kind', type=click.Choice(['dynamic', 'static', 'all']), default='all')
@click.argument(
    'group',
    default=utils.generic.get_current_group(),
    callback=utils.generic.is_valid_group)
@click.option('--check-token', is_flag=True)
@click.option(
    '--delete-pending-vulns', metavar=EXP_METAVAR, callback=_convert_exploit)
@click.option(
    '--get-static-dict',
    metavar='[<find_id> | all | local]',
    help='execute in group path')
@click.option('--report-vulns', metavar=EXP_METAVAR, callback=_convert_exploit)
def integrates_management(kind, group, check_token,
                          delete_pending_vulns, get_static_dict, report_vulns):
    """Perform operations with the Integrates API."""
    if delete_pending_vulns is not None:
        sys.exit(0 if toolbox.delete_pending_vulnerabilities(
            group, delete_pending_vulns, kind) else 1)
    elif report_vulns:
        sys.exit(0 if toolbox.report_vulnerabilities(
            group, report_vulns, kind) else 1)
    elif get_static_dict:
        sys.exit(0 if toolbox.get_static_dictionary(
            group, get_static_dict) else 1)
    elif check_token:
        from toolbox import constants
        assert constants
        sys.exit(0)


@click.command(name='analytics')
@click.option(
    '--analytics-forces-logs',
    is_flag=True,
    help='pipelines-only')
def analytics_management(analytics_forces_logs):
    if analytics_forces_logs:
        sys.exit(0 if analytics.logs.load_executions_to_database() else 1)


@click.command(name='sorts', short_help='experimental')
@click.argument(
    'group',
    default=utils.generic.get_current_group(),
    callback=utils.generic.is_valid_group)
@click.option(
    '--get-data',
    is_flag=True,
    help='get group commit data')
def sorts_management(group, get_data):
    if get_data:
        sys.exit(0 if sorts.get_data.get_project_data(group) else 1)


entrypoint.add_command(resources_management)
entrypoint.add_command(analytics_management)
entrypoint.add_command(forces_management)
entrypoint.add_command(integrates_management)
entrypoint.add_command(utils.cli.utils_management)
entrypoint.add_command(sorts_management)
entrypoint.add_command(drills.cli.drills_management)
entrypoint.add_command(misc_management)


def retry_debugging_on_failure(func):
    """Run a function ensuring the debugger output is shown on failures."""
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:  # noqa
            from toolbox import constants
            from toolbox.api import integrates
            integrates.clear_cache()

            constants.LOGGER_DEBUG = True
            func(*args, **kwargs)
    return wrapped


@retry_debugging_on_failure
def main():
    """Usual entrypoint."""
    entrypoint()
