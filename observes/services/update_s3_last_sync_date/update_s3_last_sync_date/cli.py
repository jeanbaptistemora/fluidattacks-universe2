# Standard libraries
import json

# Third party libraries
import click

# Local libraries
from update_s3_last_sync_date import db_client


@click.command()
@click.argument('group')
@click.argument('auth_file', type=click.File('r'))
def main(group: str, auth_file):
    auth = json.load(auth_file)
    db_state = db_client.make_access_point(auth)
    try:
        db_client.create_or_update(db_state, group)
    finally:
        db_client.drop_access_point(db_state)
