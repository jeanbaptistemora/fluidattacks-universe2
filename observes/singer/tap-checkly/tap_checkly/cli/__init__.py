# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from ._emitter import (
    Emitter,
)
import click
from datetime import (
    datetime,
)
from fa_purity import (
    Maybe,
)
from tap_checkly._utils import (
    DateInterval,
)
from tap_checkly.api import (
    Credentials,
)
from tap_checkly.state import (
    EtlState,
)
from tap_checkly.streams import (
    SupportedStreams,
)
from typing import (
    NoReturn,
    Optional,
)
from utils_logger.v2 import (
    start_session,
)


@click.command()  # type: ignore[misc]
@click.option("--api-user", type=str, required=True)  # type: ignore[misc]
@click.option("--api-key", type=str, required=True)  # type: ignore[misc]
@click.option("--all-streams", is_flag=True, default=False)  # type: ignore[misc]
@click.argument(  # type: ignore[misc]
    "name",
    type=click.Choice(
        [x.value for x in iter(SupportedStreams)], case_sensitive=False
    ),
    required=False,
    default=None,
)
def stream(
    name: Optional[str], api_user: str, api_key: str, all_streams: bool
) -> NoReturn:
    creds = Credentials(api_user, api_key)
    selection = (
        tuple(SupportedStreams)
        if all_streams
        else Maybe.from_optional(name)
        .map(SupportedStreams)
        .map(lambda i: (i,))
        .unwrap()
    )
    empty: Maybe[DateInterval] = Maybe.empty()
    emitter = Emitter(EtlState(empty), creds)
    emitter.emit_streams(selection).compute()


@click.group()  # type: ignore[misc]
def main() -> None:
    start_session()


main.add_command(stream)
