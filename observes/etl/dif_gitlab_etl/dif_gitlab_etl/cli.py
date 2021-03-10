# Standard libraries
import asyncio
import json
from os import (
    environ,
)
import sys
from typing import (
    IO, List,
)

# Third-Party/Observes libraries
import click
from streamer_gitlab.log import log

# Local libraries
from dif_gitlab_etl import executer


@click.command()
@click.argument('projects', nargs=-1)
@click.argument('auth_file', type=click.File('r'))
def start_etl(projects: List[str], auth_file: IO[str]) -> None:
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
def main() -> None:
    # main cli group
    pass


main.add_command(start_etl)
