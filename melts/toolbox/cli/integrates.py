# Local libraries
import sys

# Third party libraries
from click import (
    command,
    option,
)

# Local libraries
from toolbox import (
    constants,
)

EXP_METAVAR = '[<EXPLOIT | all>]'


def _convert_exploit(ctx, param, value):  # pylint: disable=unused-argument
    return '' if value == 'all' else value


@command(name='integrates', short_help='use the integrates API')
@option('--check-token', is_flag=True)
def integrates_management(check_token):
    """Perform operations with the Integrates API."""
    if check_token:
        assert constants
        sys.exit(0)
