from . import (
    _emitter,
)
from ._objs import (
    SupportedStreams,
)
from fa_purity import (
    Cmd,
)
from paginator import (
    AllPages,
)
from returns.io import (
    IO,
)
from tap_checkly.api import (
    ApiClient,
    ApiPage,
)
from typing import (
    Iterator,
)

ALL = AllPages()


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


__all__ = [
    "SupportedStreams",
]
