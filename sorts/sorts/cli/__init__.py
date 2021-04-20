# Standard libraries
import sys
import time

# Third party libraries
import click

# Local libraries
from integrates.graphql import create_session

from sorts.integrates.dal import get_user_email
from sorts.predict.commit import prioritize as prioritize_commits
from sorts.predict.file import prioritize as prioritize_files
from sorts.training.commit import get_subscription_commit_metadata
from sorts.training.file import get_subscription_file_metadata
from sorts.utils.bugs import configure_bugsnag
from sorts.utils.decorators import shield
from sorts.utils.logs import (
    log,
    log_to_remote_info,
    mixpanel_track,
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
    token: str
) -> None:
    configure_bugsnag()
    start_time: float = time.time()
    success: bool = False
    if token:
        create_session(token)
        user_email: str = get_user_email()
        if get_commit_data:
            success = get_subscription_commit_metadata(subscription)
        elif get_file_data:
            success = get_subscription_file_metadata(subscription)
        elif predict_commit:
            success = prioritize_commits(subscription)
        else:
            success = prioritize_files(subscription)

        log_to_remote_info(
            msg=f'Success: {success}',
            subscription=subscription,
            time=f'Finished after {time.time() - start_time:.2f} seconds',
            get_commit_data=get_commit_data,
            get_file_data=get_file_data,
            predict_commit=predict_commit,
            user=user_email
        )
        mixpanel_track(
            user_email,
            'sorts_execution',
            subscription=subscription,
            get_commit_data=get_commit_data,
            get_file_data=get_file_data,
            predict_commit=predict_commit
        )
    else:
        log(
            'error',
            'Set the Integrates API token either using the option '
            '--token or the environmental variable '
            'INTEGRATES_API_TOKEN'
        )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter, unexpected-keyword-arg
    execute_sorts(
        prog_name='sorts'
    )
