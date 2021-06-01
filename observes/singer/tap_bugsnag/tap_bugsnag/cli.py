import click
from tap_bugsnag import (
    executor,
)
from tap_bugsnag.api import (
    Credentials,
)
from tap_bugsnag.streams import (
    SupportedStreams,
)
from typing import (
    Optional,
)


@click.command()
@click.option("--api-key", type=str, required=True)
@click.option("--all-streams", is_flag=True, default=False)
@click.argument(
    "name",
    type=click.Choice(
        [x.value for x in iter(SupportedStreams)], case_sensitive=False
    ),
    required=False,
    default=None,
)
def stream(name: Optional[str], api_key: str, all_streams: bool) -> None:
    creds = Credentials.new(api_key)
    if name:
        executor.stream(creds, name)
    elif all_streams:
        executor.stream_all(creds)


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(stream)
