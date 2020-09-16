

# Local libraries
import sys

# Third party libraries
from click import (
    command,
    option,
)

# Local libraries
from toolbox import reports


@command(name='reports', short_help="Service reports")
@option(
    '--generate-exploits-report',
    default=''
)
def reports_management(generate_exploits_report):
    if generate_exploits_report:
        sys.exit(0 if reports.generate_exploits_report(
            generate_exploits_report) else 1)
