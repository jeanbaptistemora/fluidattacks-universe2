# Local libraries
import sys

# Third party libraries
from click import (
    command,
    option,
)

# Local libraries
from toolbox import analytics


@command(name='analytics')
@option(
    '--analytics-forces-logs',
    is_flag=True,
    help='pipelines-only')
def analytics_management(analytics_forces_logs):
    if analytics_forces_logs:
        sys.exit(0 if analytics.logs.load_executions_to_database() else 1)
