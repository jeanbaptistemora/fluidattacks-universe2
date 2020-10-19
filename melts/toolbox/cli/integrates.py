# Local libraries
import sys

# Third party libraries
from click import (
    command,
    option,
    argument,
    Choice
)

# Local libraries
from toolbox import (
    constants,
    toolbox,
    utils
)

EXP_METAVAR = '[<EXPLOIT | all>]'


def _convert_exploit(ctx, param, value):  # pylint: disable=unused-argument
    return '' if value == 'all' else value


@command(name='integrates', short_help='use the integrates API')
@argument(
    'kind', type=Choice(['dynamic', 'static', 'all']), default='all')
@argument(
    'group',
    default=utils.generic.get_current_group(),
    callback=utils.generic.is_valid_group)
@option('--check-token', is_flag=True)
@option(
    '--get-static-dict',
    metavar='[<find_id> | all | local]',
    help='execute in group path')
@option('--report-vulns', metavar=EXP_METAVAR, callback=_convert_exploit)
def integrates_management(kind, group, check_token,
                          get_static_dict, report_vulns):
    """Perform operations with the Integrates API."""
    if report_vulns:
        sys.exit(0 if toolbox.report_vulnerabilities(
            group, report_vulns, kind) else 1)
    elif get_static_dict:
        sys.exit(0 if toolbox.get_static_dictionary(
            group, get_static_dict) else 1)
    elif check_token:
        assert constants
        sys.exit(0)
