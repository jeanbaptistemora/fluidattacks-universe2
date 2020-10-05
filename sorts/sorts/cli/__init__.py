# Standard libraries
import sys
import time

# Third party libraries
import click
from aioextensions import run

# Local libraries
from utils.decorators import shield
from utils.logs import blocking_log


@click.command(
    help='File prioritizer according to the likelihood of finding '
    'a vulnerability'
)
@click.argument(
    'subscription',
    type=click.Path(
        allow_dash=False,
        dir_okay=True,
        exists=True,
        file_okay=False,
        readable=True,
        resolve_path=True,
    )
)
@click.option(
    '--get-commit-data',
    is_flag=True,
    help='Extract commit features from the subscription to train ML models')
@click.option(
    '--get-file-data',
    is_flag=True,
    help='Extract file features from the subscription to train ML models')
@click.option(
    '--predict-commit',
    is_flag=True,
    help='Use the legacy predictor that sorts files based on commit features')
def dispatch(
    subscription: str,
    get_commit_data: bool,
    get_file_data: bool,
    predict_commit: bool
) -> None:
    start_time: float = time.time()
    success: bool = run(
        main(
            subscription=subscription,
            get_commit_data=get_commit_data,
            get_file_data=get_file_data,
            predict_commit=predict_commit
        )
    )
    blocking_log(
        'info',
        'Success: %s\nProcess finished after %s seconds.',
        success,
        str(round(time.time() - start_time, 3))
    )
    sys.exit(0 if success else 1)


@shield(on_error_return=False)
async def main(
    subscription: str,
    get_commit_data: bool,
    get_file_data: bool,
    predict_commit: bool
) -> bool:
    if get_commit_data:
        pass
    elif get_file_data:
        pass
    elif predict_commit:
        pass
    else:
        print(subscription)
    return True
