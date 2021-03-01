# Standard libraries
import json
from typing import (
    AnyStr,
    IO,
)

# Third party libraries
import click

# Local libraries
from tap_mailchimp import (
    api,
    auth,
    streams
)


ApiClient = api.ApiClient
Credentials = auth.Credentials
STREAM_EXECUTOR = streams.STREAM_EXECUTOR
SupportedStreams = streams.SupportedStreams


@click.command()
@click.option('--creds-file', type=click.File('r'), required=True)
@click.option(
    '--stream-name',
    type=click.Choice(
        list(map(lambda x: x.value, iter(SupportedStreams))),
        case_sensitive=False),
    required=True
)
def stream(creds_file: IO[AnyStr], stream_name: str) -> None:
    creds: Credentials = auth.to_credentials(json.load(creds_file))
    client: ApiClient = api.new_client(creds)
    STREAM_EXECUTOR[SupportedStreams(stream_name)](client, None)


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(stream)
