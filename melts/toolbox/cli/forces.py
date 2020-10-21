# Standard libraries
import sys
import os

# Third party libraries
from click import (
    argument,
    BadArgumentUsage,
    command,
    Choice,
    option
)

# Local libraries
from toolbox import (
    forces,
    toolbox,
    utils,
)

EXP_METAVAR = '[<EXPLOIT | all>]'


def _convert_exploit(ctx, param, value):  # pylint: disable=unused-argument
    return '' if value == 'all' else value


@command(name='forces', short_help='use the exploits')
@argument(
    'group',
    default=utils.generic.get_current_group(),
    callback=utils.generic.is_valid_group)
@option(
    '--check-sync',
    '--sync',
    metavar=EXP_METAVAR,
    help='check if exploits results are the same as on Integrates',
    callback=_convert_exploit)
@option(
    '--decrypt', is_flag=True, help='decrypt the secrets of a group')
@option(
    '--encrypt', is_flag=True, help='encrypt the secrets of a group')
@option('--fill-with-iexps', is_flag=True)
@option('--generate-exploits', is_flag=True)
@option('--get-vulns', type=Choice(['dynamic', 'static', 'all']))
@option(
    '--lint-exps',
    metavar=EXP_METAVAR,
    help='lint exploits for a group',
    callback=_convert_exploit)
@option('--lint-changed-exploits', is_flag=True)
@option('--run-exps', '--run', '-r', is_flag=True, help='run exploits')
@option(
    '--static',
    '-s',
    metavar=EXP_METAVAR,
    help='run a static exploit',
    callback=_convert_exploit)
@option(
    '--dynamic',
    '-d',
    metavar=EXP_METAVAR,
    help='run a dynamic exploit',
    callback=_convert_exploit)
@option('--upload-exps-from-repo-to-integrates', is_flag=True)
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
        raise BadArgumentUsage(
            f'{group} group has no forces')

    # This allows linters to see the resources folder
    sys.path.append(os.path.join(
        os.getcwd(), 'groups', group, 'forces', 'dynamic', 'resources'))
    sys.path.append(os.path.join(
        os.getcwd(), 'groups', group, 'forces', 'static', 'resources'))

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
