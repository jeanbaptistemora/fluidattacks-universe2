# Standard libraries

# Third party libraries
import click

# Local libraries


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

    if get_commit_data:
        pass
    elif get_file_data:
        pass
    elif predict_commit:
        pass
    else:
        print(subscription)
