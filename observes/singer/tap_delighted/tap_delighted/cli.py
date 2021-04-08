# Standard libraries
from typing import (
    Optional,
)

# Third party libraries
import click

# Local libraries
from tap_delighted import (
    executor,
)
from tap_delighted.auth import (
    Credentials,
)
from tap_delighted.streams import (
    SupportedStreams,
)


@click.command()
@click.option('--api-key', type=str, required=True)
@click.option('--all-streams', is_flag=True, default=False)
@click.option(
    '--name',
    type=click.Choice(
        [x.value for x in iter(SupportedStreams)],
        case_sensitive=False),
    required=False,
    default=None
)
def stream(
    api_key: str,
    name: Optional[str],
    all_streams: bool
) -> None:
    creds = Credentials.new(api_key)
    if all_streams:
        executor.stream_all(creds)
    elif name:
        executor.stream(creds, name)


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(stream)
