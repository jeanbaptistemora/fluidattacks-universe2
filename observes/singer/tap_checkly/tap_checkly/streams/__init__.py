# Standard libraries
from typing import (
    Iterator,
)

# Third party libraries
from returns.curry import (
    partial,
)

# Local libraries
from paginator import (
    AllPages,
)
from tap_checkly.api import (
    ApiClient,
    ApiPage,
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
    pages: Iterator[ApiPage],
) -> None:
    for page in pages:
        emitter.emit_page(stream, page)


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


def all_chk_status(api: ApiClient) -> None:
    stream = SupportedStreams.CHECK_STATUS
    status = api.checks.list_check_status()
    status.data.map(
        partial(emitter.emit_records, stream)
    )


def all_dashboards(api: ApiClient) -> None:
    _stream_data(
        SupportedStreams.DASHBOARD,
        api.dashboards.list_dashboards(ALL),
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
