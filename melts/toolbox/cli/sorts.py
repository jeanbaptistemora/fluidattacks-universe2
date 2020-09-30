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
    help='Extract commit features from the subscription to train ML models')
@option(
    '--get-file-data',
    is_flag=True,
    help='Extract file features from the subscription to train ML models')
@option(
    '--predict-commit',
    is_flag=True,
    help='Use the legacy predictor that sorts files based on commit features')
def sorts_management(
    group,
    get_commit_data,
    get_file_data,
    predict_commit
):
    if get_commit_data:
        sys.exit(0 if sorts.get_data.get_project_data(group, 'commit') else 1)
    elif get_file_data:
        sys.exit(0 if sorts.get_data.get_project_data(group, 'file') else 1)
    elif predict_commit:
        sys.exit(0 if sorts.predict.predict_commit(group) else 1)
    else:
        sys.exit(0 if sorts.predict.predict_file(group) else 1)
