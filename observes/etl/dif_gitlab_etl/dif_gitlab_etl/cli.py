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
    env_vars = {
        'AUTONOMIC_API_TOKEN': environ.get('AUTONOMIC_API_TOKEN', None),
        'SERVICES_API_TOKEN': environ.get('SERVICES_API_TOKEN', None),
        'PRODUCT_API_TOKEN': environ.get('PRODUCT_API_TOKEN', None),
    }
    if not all(env_vars.values()):
        missing = filter(lambda x: bool(x[1]) is False, env_vars.items())
        missing_vars = list(map(lambda x: x[0], missing))
        log('critical', f'Env vars {str(missing_vars)} are missing/empty')
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
