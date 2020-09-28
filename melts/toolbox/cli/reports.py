

# Local libraries
import sys

# Third party libraries
from click import (
    command,
    option,
)

# Local libraries
from toolbox.reports import (
    exploits,
)


@command(name='reports', short_help="Service reports")
@option('--generate-exploits-report', 'o_generate_exploits_report',
        default='')
def reports_management(
    o_generate_exploits_report,
):
    success: bool = True

    if o_generate_exploits_report:
        success = exploits.generate_exploits_report(
            o_generate_exploits_report)

    sys.exit(0 if success else 1)
