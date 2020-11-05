# Standard libraries
import json
from typing import Any, Dict
# Third party libraries
import click
# Local libraries
from dif_dynamo_etl import etl


@click.command()
@click.argument('auth_file', type=click.File('r'))
def live_stream_etl(auth_file):
    json.load(auth_file)


@click.command()
@click.argument('auth_file', type=click.File('r'))
def new_data_etl(auth_file):
    auth: Dict[str, Any] = json.load(auth_file)
    etl.start_new_data_etl(auth)


@click.command()
@click.argument('auth_file', type=click.File('r'))
def old_data_etl(auth_file):
    auth: Dict[str, Any] = json.load(auth_file)
    etl.start_old_data_etl(auth)


@click.group()
def main():
    pass


main.add_command(live_stream_etl)
main.add_command(new_data_etl)
main.add_command(old_data_etl)
