# Local libraries
import sys

# Third party libraries
from click import (
    argument,
    command,
    option,
)

# Local libraries
from toolbox import (
    sorts
)


@command(name='sorts', short_help='experimental')
@argument(
    'group',
)
@option(
    '--get-commit-data',
    is_flag=True,
    help='get group commit data')
@option(
    '--get-file-data',
    is_flag=True,
    help='get group file data')
@option(
    '--predict',
    is_flag=True,
    help="predict vuln likelihood in group's commits")
def sorts_management(group, get_commit_data, get_file_data, predict):
    if get_commit_data:
        sys.exit(0 if sorts.get_data.get_project_data(group, 'commit') else 1)
    if get_file_data:
        sys.exit(0 if sorts.get_data.get_project_data(group, 'file') else 1)
    if predict:
        sys.exit(0 if sorts.predict.predict(group) else 1)
