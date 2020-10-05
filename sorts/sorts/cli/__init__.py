# Standard libraries
import os
import sys
import time
from typing import Optional

# Third party libraries
import click
from aioextensions import run

# Local libraries
from integrates.domain import get_vulnerable_lines
from integrates.graphql import create_session
from utils.decorators import shield
from utils.logs import (
    blocking_log,
    log,
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
def dispatch(
    subscription: str,
    get_commit_data: bool,
    get_file_data: bool,
    predict_commit: bool,
    token: Optional[str]
) -> None:
    start_time: float = time.time()
    success: bool = run(
        main(
            subscription=subscription,
            get_commit_data=get_commit_data,
            get_file_data=get_file_data,
            predict_commit=predict_commit,
            token=token
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
    predict_commit: bool,
    token: Optional[str]
) -> bool:
    if get_commit_data:
        pass
    elif get_file_data:
        pass
    elif predict_commit:
        pass
    else:
        if token:
            create_session(token)
            group: str = os.path.basename(os.path.normpath(subscription))
            vulnerabilities = await get_vulnerable_lines(group)
            await log('info', 'Query result: %s', vulnerabilities)
    return True
