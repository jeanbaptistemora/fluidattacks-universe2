from . import (
    _streams,
)
import click
from tap_mandrill.api import (
    ApiClient,
    ApiKey,
)
from tap_mandrill.singer.core import (
    DataStreams,
)
from typing import (
    NoReturn,
)


@click.command("stream")  # type: ignore[misc]
@click.option("--api-key", type=str, required=True)  # type: ignore[misc]
@click.argument(  # type: ignore[misc]
    "stream",
    type=click.Choice(
        [x.value for x in iter(DataStreams)],
        case_sensitive=False,
    ),
    required=True,
)
def stream_cli(api_key: str, stream: str) -> NoReturn:
    key = ApiKey.protect(api_key)
    client = ApiClient(key)
    _streams.emit_stream(client, DataStreams(stream)).compute()


@click.group()  # type: ignore[misc]
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(stream_cli)
