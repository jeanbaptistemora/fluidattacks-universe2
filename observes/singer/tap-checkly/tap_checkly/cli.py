import click
from fa_purity import (
    Maybe,
)
from tap_checkly import (
    executor,
)
from tap_checkly.api import (
    Credentials,
)
from tap_checkly.streams import (
    SupportedStreams,
)
from typing import (
    Optional,
)
from utils_logger.v2 import (
    start_session,
)


@click.command()  # type: ignore[misc]
@click.option("--api-user", type=str, required=True)
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
def stream(
    name: Optional[str], api_user: str, api_key: str, all_streams: bool
) -> None:
    creds = Credentials(api_user, api_key)
    selection = (
        tuple(SupportedStreams)
        if all_streams
        else Maybe.from_optional(name)
        .map(SupportedStreams)
        .map(lambda i: (i,))
        .unwrap()
    )
    executor.emit_streams(creds, selection)


@click.group()  # type: ignore[misc]
def main() -> None:
    start_session()


main.add_command(stream)
