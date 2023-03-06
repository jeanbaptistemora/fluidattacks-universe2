from ._emitter import (
    Emitter,
)
import click
from datetime import (
    datetime,
)
from fa_purity import (
    Cmd,
    Maybe,
)
from fa_purity.date_time import (
    DatetimeFactory,
    DatetimeTZ,
)
from fa_purity.json.factory import (
    load,
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
    decode_state,
    SupportedStreams,
)
from typing import (
    NoReturn,
    Optional,
)
from utils_logger.v2 import (
    start_session,
)


def _decode_state(file_path: str) -> Cmd[EtlState]:
    def _action() -> EtlState:
        with open(file_path, "r") as file:
            raw = load(file).unwrap()
        return decode_state(raw).unwrap()

    return Cmd.from_cmd(_action)


@click.command()  # type: ignore[misc]
@click.option("--api-user", type=str, required=True)  # type: ignore[misc]
@click.option("--api-key", type=str, required=True)  # type: ignore[misc]
@click.option("--reports-start", type=str, required=True)  # type: ignore[misc]
@click.option("--all-streams", is_flag=True, default=False)  # type: ignore[misc]
@click.option("--state", type=click.Path(exists=True), default=None)  # type: ignore[misc]
@click.argument(  # type: ignore[misc]
    "name",
    type=click.Choice(
        [x.value for x in iter(SupportedStreams)], case_sensitive=False
    ),
    required=False,
    default=None,
)
def stream(
    name: Optional[str],
    api_user: str,
    api_key: str,
    all_streams: bool,
    state: Optional[str],
    reports_start: str,
) -> NoReturn:
    creds = Credentials(api_user, api_key)
    selection = (
        tuple(SupportedStreams)
        if all_streams
        else Maybe.from_optional(name)
        .map(SupportedStreams)
        .map(lambda i: (i,))
        .to_result()
        .alt(lambda _: ValueError("Null stream selection"))
        .unwrap()
    )
    empty: Maybe[DateInterval] = Maybe.empty()
    _state = (
        _decode_state(state)
        if state
        else Cmd.from_cmd(lambda: EtlState(empty))
    )
    _reports_start = DatetimeTZ.assert_tz(
        datetime.strptime(reports_start, "%Y-%m-%d %H:%M:%S %z")
    ).unwrap()
    cmd: Cmd[None] = _state.bind(
        lambda s: Emitter(
            s, creds, DatetimeFactory.to_utc(_reports_start)
        ).emit_streams(selection)
    )
    cmd.compute()


@click.group()  # type: ignore[misc]
def main() -> None:
    start_session()


main.add_command(stream)
