from . import (
    _emitter,
)
from ._objs import (
    SupportedStreams,
)
from fa_purity import (
    Cmd,
    Stream,
)
from fa_purity.stream.transform import (
    chain,
    consume,
)
from fa_singer_io.singer import (
    emitter,
    SingerRecord,
)
from paginator import (
    AllPages,
)
from returns.io import (
    IO,
)
import sys
from tap_checkly.api2.alert_channels import (
    AlertChannelsClient,
)
from tap_checkly.api2.checks import (
    ChecksClient,
)
from tap_checkly.api2.id_objs import (
    IndexedObj,
)
from tap_checkly.api import (
    ApiClient,
    ApiPage,
)
from tap_checkly.singer.alert_channels.records import (
    alert_ch_records,
)
from tap_checkly.singer.checks.results.records import (
    encode_result,
    encode_rolled,
)
from typing import (
    Iterator,
)

ALL = AllPages()


def _emit_stream(
    records: Stream[SingerRecord],
) -> Cmd[None]:
    emissions = records.map(lambda s: emitter.emit(sys.stdout, s))
    return consume(emissions)


def _stream_data(
    stream: SupportedStreams,
    pages: Iterator[IO[ApiPage]],
) -> Cmd[None]:
    def action() -> None:
        for page in pages:
            _emitter.emit_iopage(stream, page)

    return Cmd.from_cmd(action)


def all_checks(api: ApiClient) -> Cmd[None]:
    return _stream_data(
        SupportedStreams.CHECKS,
        api.checks.list_checks(ALL),
    )


def all_chk_groups(api: ApiClient) -> Cmd[None]:
    return _stream_data(
        SupportedStreams.CHECK_GROUPS,
        api.checks.list_check_groups(ALL),
    )


def all_chk_reports(api: ApiClient) -> Cmd[None]:
    return _stream_data(
        SupportedStreams.REPORTS,
        iter([api.checks.list_reports()]),
    )


def all_chk_status(api: ApiClient) -> Cmd[None]:
    stream = SupportedStreams.CHECK_STATUS

    def action() -> None:
        api.checks.list_check_status().map(
            lambda status: _emitter.emit_records(stream, status.data)
        )

    return Cmd.from_cmd(action)


def all_dashboards(api: ApiClient) -> Cmd[None]:
    return _stream_data(
        SupportedStreams.DASHBOARD,
        api.dashboards.list_dashboards(ALL),
    )


def all_env_vars(api: ApiClient) -> Cmd[None]:
    return _stream_data(
        SupportedStreams.ENV_VARS,
        api.env.list_env_vars(ALL),
    )


def all_maint_windows(api: ApiClient) -> Cmd[None]:
    return _stream_data(
        SupportedStreams.MAINTENACE_WINDOWS,
        api.maintenance.list_mant_windows(ALL),
    )


def all_snippets(api: ApiClient) -> Cmd[None]:
    return _stream_data(
        SupportedStreams.SNIPPETS,
        api.snippets.list_snippets(ALL),
    )


def check_results(client: ChecksClient) -> Cmd[None]:
    return _emit_stream(
        client.list_ids()
        .bind(
            lambda c: client.list_check_results(c).map(
                lambda r: IndexedObj(c, r)
            )
        )
        .map(encode_result)
        .transform(chain),
    )


def rolled_results(client: ChecksClient) -> Cmd[None]:
    return _emit_stream(
        client.list_ids()
        .bind(
            lambda c: client.list_rolled_results(c).map(
                lambda r: IndexedObj(c, r)
            )
        )
        .map(encode_rolled)
        .transform(chain),
    )


def alert_chs(client: AlertChannelsClient) -> Cmd[None]:
    return _emit_stream(
        client.list_all().map(alert_ch_records).transform(chain),
    )


__all__ = [
    "SupportedStreams",
]
