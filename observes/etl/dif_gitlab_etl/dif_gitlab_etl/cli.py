# Standard libraries
import asyncio
import json
from os import (
    environ,
)
import sys
from typing import (
    List,
)

# Third party libraries
import click

# Local libraries
from dif_gitlab_etl import executer
from streamer_gitlab.log import log


@click.command()
@click.argument('projects', nargs=-1)
@click.argument('auth_file', type=click.File('r'))
def start_etl(projects: List[str], auth_file):
    try:
        environ['GITLAB_API_TOKEN']
    except KeyError:
        log('critical', 'Export GITLAB_API_TOKEN as environment variable')
        sys.exit(1)
    else:
        auth = json.load(auth_file)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            executer.start_etls(projects, auth)
        )


@click.group()
def main():
    pass


main.add_command(start_etl)
