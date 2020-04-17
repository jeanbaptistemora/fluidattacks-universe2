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
)
from .drills import drills_management
from .misc import misc_management


EXP_METAVAR = '[<EXPLOIT | all>]'
SUBS_METAVAR = '[SUBSCRIPTION]'


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
    'subscription',
    default=utils.get_current_subscription(),
    callback=utils.is_valid_subscription)
@click.option(
    '--check-repos',
    default=utils.get_current_subscription(),
    metavar=SUBS_METAVAR)
@click.option(
    '--clone-from-customer-git',
    'clone',
    is_flag=True,
    help='clone the repositories of a subscription')
@click.option('--does-subs-exist', 'subs_exist', metavar=SUBS_METAVAR)
@click.option(
    '--fingerprint',
    is_flag=True,
    help='get the fingerprint of a subscription')
@click.option('--login', is_flag=True, help='login to AWS through OKTA')
@click.option(
    '--mailmap',
    '-mp',
    is_flag=True,
    help='check if the mailmap of a subscription is valid')
@click.option(
    '--edit', is_flag=True, help='edit the secrets of a subscription')
@click.option(
    '--read', is_flag=True, help='read the secrets of a subscription')
@click.option('--push-repos', is_flag=True)
@click.option('--pull-repos', is_flag=True)
def resources_management(subscription, check_repos, clone, fingerprint,
                         mailmap, login, subs_exist, edit, read, push_repos,
                         pull_repos):
    """Allows administration tasks within subscriptions"""
    if mailmap:
        sys.exit(0 if resources.check_mailmap(subscription) else 1)
    elif clone:
        sys.exit(0 if resources.repo_cloning(subscription) else 1)
    elif fingerprint:
        sys.exit(0 if resources.get_fingerprint(subscription) else 1)
    elif edit:
        sys.exit(0 if resources.edit_secrets(subscription) else 1)
    elif read:
        sys.exit(0 if resources.read_secrets(subscription) else 1)
    elif push_repos:
        sys.exit(0 if resources.sync_repositories_to_s3(subscription) else 1)
    elif pull_repos:
        sys.exit(0 if resources.sync_s3_to_fusion(subscription) else 1)
    elif subs_exist:
        sys.exit(0 if toolbox.does_subs_exist(subs_exist) else 1)
    elif login:
        sys.exit(0 if resources.utils.okta_aws_login(
            f'continuous-{subscription}') else 1)
    elif check_repos != 'unspecified-subs':
        sys.exit(0 if resources.check_repositories(check_repos) else 1)


@click.command(name='forces', short_help='use the exploits')
@click.argument(
    'subscription',
    default=utils.get_current_subscription(),
    callback=utils.is_valid_subscription)
@click.option(
    '--check-sync',
    '--sync',
    metavar=EXP_METAVAR,
    help='check if exploits results are the same as on Integrates',
    callback=_convert_exploit)
@click.option(
    '--decrypt', is_flag=True, help='decrypt the secrets of a subscription')
@click.option(
    '--encrypt', is_flag=True, help='encrypt the secrets of a subscription')
@click.option('--init-secrets', '--init', is_flag=True)
@click.option('--fill-with-mocks', is_flag=True)
@click.option('--generate-exploits', is_flag=True)
@click.option('--get-vulns', type=click.Choice(['dynamic', 'static', 'all']))
@click.option(
    '--lint-exps',
    metavar=EXP_METAVAR,
    help='lint exploits for a subscription',
    callback=_convert_exploit)
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
def forces_management(subscription, check_sync, decrypt,
                      encrypt, init_secrets, fill_with_mocks, get_vulns,
                      generate_exploits, lint_exps, run_exps, static, dynamic):
    """Perform operations with the forces service."""
    if not toolbox.has_break_build(subscription):
        raise click.BadArgumentUsage(
            f'{subscription} subscription has no break-build')
    if run_exps:
        if dynamic is not None:
            sys.exit(0 if toolbox.run_dynamic_exploits(subscription, dynamic)
                     else 1)
        elif static is not None:
            sys.exit(0 if toolbox.run_static_exploits(subscription, static)
                     else 1)
    elif check_sync is not None:
        success = forces.sync.are_exploits_synced(subscription, check_sync)
        sys.exit(0 if success else 1)
    elif fill_with_mocks:
        toolbox.fill_with_mocks(
            subs_glob=(subscription or '*'), create_files=True)
    elif generate_exploits:
        toolbox.generate_exploits(subs_glob=(subscription or '*'))
    elif get_vulns:
        sys.exit(0 if toolbox.get_vulnerabilities_yaml(subscription,
                                                       get_vulns) else 1)
    elif lint_exps is not None:
        sys.exit(0 if toolbox.lint_exploits(subscription, lint_exps) else 1)
    elif decrypt:
        sys.exit(0 if toolbox.decrypt_secrets(subscription) else 1)
    elif encrypt:
        sys.exit(0 if toolbox.encrypt_secrets(subscription) else 1)
    elif init_secrets:
        sys.exit(0 if toolbox.init_secrets(subscription) else 1)


@click.command(name='integrates', short_help='use the integrates API')
@click.argument(
    'kind', type=click.Choice(['dynamic', 'static', 'all']), default='all')
@click.argument(
    'subscription',
    default=utils.get_current_subscription(),
    callback=utils.is_valid_subscription)
@click.option('--check-token', is_flag=True)
@click.option(
    '--delete-pending-vulns', metavar=EXP_METAVAR, callback=_convert_exploit)
@click.option(
    '--get-static-dict',
    metavar='[<find_id> | all | local]',
    help='execute in subscription path')
@click.option('--report-vulns', metavar=EXP_METAVAR, callback=_convert_exploit)
def integrates_management(kind, subscription, check_token,
                          delete_pending_vulns, get_static_dict, report_vulns):
    """Perform operations with the Integrates API."""
    if delete_pending_vulns is not None:
        sys.exit(0 if toolbox.delete_pending_vulnerabilities(
            subscription, delete_pending_vulns, kind) else 1)
    elif report_vulns:
        sys.exit(0 if toolbox.report_vulnerabilities(
            subscription, report_vulns, kind) else 1)
    elif get_static_dict:
        sys.exit(0 if toolbox.get_static_dictionary(
            subscription, get_static_dict) else 1)
    elif check_token:
        from toolbox import constants
        assert constants
        sys.exit(0)


@click.command(name='analytics')
@click.option(
    '--analytics-break-build-logs',
    is_flag=True,
    help='pipelines-only')
def analytics_management(analytics_break_build_logs):
    if analytics_break_build_logs:
        sys.exit(0 if analytics.logs.load_executions_to_database() else 1)


@click.command(name='utils')
@click.argument(
    'subscription',
    default=utils.get_current_subscription(),
    callback=utils.is_valid_subscription)
@click.option(
    '--get-commit-subs',
    help='get the subscription name from the commmit msg.',
    is_flag=True)
@click.option('--is-valid-commit', is_flag=True, help='pipelines-only')
@click.option(
    '--commit-exp',
    is_flag=True,
    help='check if an exploit commit meets the required criteria')
@click.option(
    '--vpn',
    is_flag=True)
def utils_management(subscription, get_commit_subs,
                     is_valid_commit, vpn, commit_exp):
    if is_valid_commit:
        sys.exit(0 if toolbox.is_valid_commit() else 1)
    elif vpn and subscription != 'unspecified-subs':
        sys.exit(0 if resources.vpn(subscription) else 1)
    elif get_commit_subs:
        subs = toolbox.get_subscription_from_commit_msg()
        click.echo(subs)
        sys.exit(0 if subs else 1)
    elif commit_exp:
        sys.exit(0 if utils.valid_commit_exp() else 1)


@click.command(name='sorts', short_help='experimental')
@click.argument(
    'subscription',
    default=utils.get_current_subscription(),
    callback=utils.is_valid_subscription)
@click.option(
    '--get-data',
    is_flag=True,
    help='get subscription commit data')
def sorts_management(subscription, get_data):
    if get_data:
        sys.exit(0 if sorts.get_data.get_project_data(subscription) else 1)


entrypoint.add_command(resources_management)
entrypoint.add_command(analytics_management)
entrypoint.add_command(forces_management)
entrypoint.add_command(integrates_management)
entrypoint.add_command(utils_management)
entrypoint.add_command(sorts_management)
entrypoint.add_command(drills_management)
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
