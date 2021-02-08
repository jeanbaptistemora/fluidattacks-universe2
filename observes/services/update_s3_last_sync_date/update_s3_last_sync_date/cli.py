# Standard libraries
import json
from typing import IO

# Third party libraries
import click

# Local libraries
from update_s3_last_sync_date import db_client


def update_job(auth_file: IO[str], job_name: str) -> None:
    auth = json.load(auth_file)
    db_state = db_client.make_access_point(auth)
    try:
        db_client.create_or_update_job(db_state, job_name)
    finally:
        db_client.drop_access_point(db_state)


@click.command()
@click.argument('auth_file', type=click.File('r'))
@click.argument('group')
def mirror(auth_file: IO[str], group: str) -> None:
    auth = json.load(auth_file)
    db_state = db_client.make_access_point(auth)
    try:
        db_client.create_or_update_group(db_state, group, 'last_sync_date')
    finally:
        db_client.drop_access_point(db_state)


@click.command()
@click.argument('auth_file', type=click.File('r'))
def formstack(auth_file: IO[str]) -> None:
    update_job(auth_file, 'formstack')


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(mirror)
main.add_command(formstack)
