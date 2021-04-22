# Standard libraries
from typing import (
    Iterator,
)

# Third party libraries
from returns.io import (
    IO,
)

# Local libraries
from paginator import (
    AllPages,
)
from tap_checkly.api import (
    ApiClient,
    ApiPage,
    CheckId,
)
from tap_checkly.streams import (
    emitter,
)
from tap_checkly.streams.objs import (
    SupportedStreams,
)


ALL = AllPages()


def _stream_data(
    stream: SupportedStreams,
    pages: Iterator[IO[ApiPage]],
) -> None:
    for page in pages:
        emitter.emit_iopage(stream, page)


def all_alerts(api: ApiClient) -> None:
    _stream_data(
        SupportedStreams.ALERT_CHS,
        api.alerts.list_alerts_channels(ALL),
    )


def all_checks(api: ApiClient) -> None:
    _stream_data(
        SupportedStreams.CHECKS,
        api.checks.list_checks(ALL),
    )


def all_chk_groups(api: ApiClient) -> None:
    _stream_data(
        SupportedStreams.CHECK_GROUPS,
        api.checks.list_check_groups(ALL),
    )


def all_chk_results(api: ApiClient) -> None:
    stream = SupportedStreams.CHECK_RESULTS

    def _emmit(checks: Iterator[CheckId]) -> None:
        for check in checks:
            _stream_data(
                stream,
                api.checks.list_check_results(check, ALL)
            )
    chks_pages_io = api.checks.list_checks(ALL)
    for chks_page_io in chks_pages_io:
        chks_page_io.map(CheckId.new).map(_emmit)


def all_chk_status(api: ApiClient) -> None:
    stream = SupportedStreams.CHECK_STATUS
    status_io = api.checks.list_check_status()
    status_io.map(
        lambda status: emitter.emit_records(stream, status.data)
    )


def all_dashboards(api: ApiClient) -> None:
    _stream_data(
        SupportedStreams.DASHBOARD,
        api.dashboards.list_dashboards(ALL),
    )


def all_env_vars(api: ApiClient) -> None:
    _stream_data(
        SupportedStreams.ENV_VARS,
        api.env.list_env_vars(ALL),
    )


def all_maint_windows(api: ApiClient) -> None:
    _stream_data(
        SupportedStreams.MAINTENACE_WINDOWS,
        api.maintenance.list_mant_windows(ALL),
    )


def all_snippets(api: ApiClient) -> None:
    _stream_data(
        SupportedStreams.SNIPPETS,
        api.snippets.list_snippets(ALL),
    )


__all__ = [
    'SupportedStreams',
]
