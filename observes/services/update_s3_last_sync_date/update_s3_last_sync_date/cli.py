# Standard libraries
import json
from typing import IO

# Third party libraries
import click

# Local libraries
from update_s3_last_sync_date import db_client


@click.command()
@click.argument('auth_file', type=click.File('r'))
@click.argument('group')
def main(auth_file: IO[str], group: str) -> None:
    auth = json.load(auth_file)
    db_state = db_client.make_access_point(auth)
    try:
        db_client.create_or_update(db_state, group)
    finally:
        db_client.drop_access_point(db_state)
