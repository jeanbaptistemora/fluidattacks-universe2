# Standard libraries
import sys
import time
from typing import Optional

# Third party libraries
import click

# Local libraries
from integrates.graphql import create_session
from training.file import get_project_data
from utils.decorators import shield
from utils.logs import log


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
@click.option(
    '--token',
    envvar='INTEGRATES_API_TOKEN',
    help='Integrates API token.',
    show_envvar=True,
)
@shield(on_error_return=False)
def execute_sorts(
    subscription: str,
    get_commit_data: bool,
    get_file_data: bool,
    predict_commit: bool,
    token: Optional[str]
) -> None:
    start_time: float = time.time()
    success: bool = False
    if get_commit_data:
        pass
    elif get_file_data:
        pass
    elif predict_commit:
        pass
    else:
        if token:
            create_session(token)
            success = get_project_data(subscription)
        else:
            log(
                'error',
                'Set the Integrates API token either using the option --token '
                'or the environmental variable INTEGRATES_API_TOKEN'
            )
    log(
        'info',
        'Success: %s\nProcess finished after %.2f seconds.',
        success,
        time.time() - start_time
    )
    sys.exit(0 if success else 1)
