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


def _stream_data(
    stream: SupportedStreams,
    pages: Iterator[ApiPage],
) -> None:
    for page in pages:
        emitter.emit_page(stream, page)


def all_alerts(api: ApiClient) -> None:
    _stream_data(
        SupportedStreams.ALERT_CHS,
        api.alerts.list_alerts_channels(AllPages()),
    )


def all_chk_groups(api: ApiClient) -> None:
    _stream_data(
        SupportedStreams.CHECK_GROUPS,
        api.checks.list_check_groups(AllPages()),
    )


__all__ = [
    'SupportedStreams',
]
