# Standard libraries
import sys
import time
from typing import Optional

# Third party libraries
import click

# Local libraries
from integrates.graphql import create_session
from predict.commit import prioritize as prioritize_commits
from predict.file import prioritize as prioritize_files
from training.commit import get_subscription_commit_metadata
from training.file import get_subscription_file_metadata
from utils.bugs import configure_bugsnag
from utils.decorators import shield
from utils.logs import log
from utils.version import check_version_is_latest


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
    configure_bugsnag()
    start_time: float = time.time()
    success: bool = False
    if not check_version_is_latest():
        log(
            'warning',
            'There is a newer version available for download\n\n\t\t'
            'pip install -U sorts\n'
        )
    if get_commit_data:
        if token:
            create_session(token)
            success = get_subscription_commit_metadata(subscription)
        else:
            log(
                'error',
                'Set the Integrates API token either using the option '
                '--token or the environmental variable '
                'INTEGRATES_API_TOKEN'
            )
    elif get_file_data:
        if token:
            create_session(token)
            success = get_subscription_file_metadata(subscription)
        else:
            log(
                'error',
                'Set the Integrates API token either using the option '
                '--token or the environmental variable '
                'INTEGRATES_API_TOKEN'
            )
    elif predict_commit:
        success = prioritize_commits(subscription)
    else:
        success = prioritize_files(subscription)
    log('info', 'Success: %s', success)
    log('info', 'Finished after %.2f seconds.', time.time() - start_time)
    sys.exit(0 if success else 1)
