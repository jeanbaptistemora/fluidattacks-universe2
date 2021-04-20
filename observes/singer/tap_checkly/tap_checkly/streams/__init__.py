# Local libraries
from typing import Iterator
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


def all_chk_groups(api: ApiClient) -> None:
    _stream_data(
        SupportedStreams.CHECK_GROUPS,
        api.checks.list_check_groups(ALL),
    )


def all_checks(api: ApiClient) -> None:
    _stream_data(
        SupportedStreams.CHECKS,
        api.checks.list_checks(ALL),
    )


__all__ = [
    'SupportedStreams',
]
