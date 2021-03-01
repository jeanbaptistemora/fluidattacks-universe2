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
stream_executor = streams.stream_executor
SupportedStreams = streams.SupportedStreams


@click.command()
@click.option('--creds-file', type=click.File('r'), required=True)
@click.option(
    '--stream-name',
    type=click.Choice(
        [x.value for x in iter(SupportedStreams)],
        case_sensitive=False),
    required=True
)
def stream(creds_file: IO[AnyStr], stream_name: str) -> None:
    creds: Credentials = auth.to_credentials(json.load(creds_file))
    client: ApiClient = api.new_client(creds)
    stream_executor[SupportedStreams(stream_name)](client, None)


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(stream)
