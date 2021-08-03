import click
from singer_io.singer2.json import (
    JsonFactory,
)
from tap_mailchimp import (
    auth,
    executor,
)
from tap_mailchimp.auth import (
    Credentials,
)
from tap_mailchimp.streams import (
    SupportedStreams,
)
from typing import (
    IO,
    Optional,
)


@click.command()
@click.option("--creds-file", type=click.File("r", "UTF-8"), required=True)
@click.option("--all-streams", is_flag=True, default=False)
@click.option(
    "--name",
    type=click.Choice(
        [x.value for x in iter(SupportedStreams)], case_sensitive=False
    ),
    required=False,
    default=None,
)
def stream(
    creds_file: IO[str], name: Optional[str], all_streams: bool
) -> None:
    creds: Credentials = auth.to_credentials(JsonFactory.load(creds_file))
    if all_streams:
        executor.stream_all(creds)
    elif name:
        executor.stream(creds, name)


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(stream)
