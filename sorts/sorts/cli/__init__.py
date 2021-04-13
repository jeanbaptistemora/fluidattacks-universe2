# Standard libraries
import sys
import time
from typing import Optional

# Third party libraries
import click

# Local libraries
from integrates.graphql import create_session

from sorts.predict.commit import prioritize as prioritize_commits
from sorts.predict.file import prioritize as prioritize_files
from sorts.training.commit import get_subscription_commit_metadata
from sorts.training.file import get_subscription_file_metadata
from sorts.utils.bugs import configure_bugsnag
from sorts.utils.decorators import shield
from sorts.utils.logs import (
    log,
    log_to_remote_info
)


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
    log_to_remote_info(
        msg=f'Success: {success}',
        subscription=subscription,
        time=f'Finished after {time.time() - start_time} seconds',
        get_commit_data=get_commit_data,
        get_file_data=get_file_data,
        predict_commit=predict_commit
    )
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter, unexpected-keyword-arg
    execute_sorts(
        prog_name='sorts'
    )
