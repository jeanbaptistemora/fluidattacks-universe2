# Local libraries
from paginator import (
    AllPages,
)
from tap_checkly.api import (
    ApiClient,
)
from tap_checkly.streams import (
    emitter,
)

from tap_checkly.streams.objs import (
    SupportedStreams,
)


def all_alerts(api: ApiClient) -> None:
    stream = SupportedStreams.ALERT_CHS
    pages = api.alerts.list_alerts_channels(AllPages())
    for page in pages:
        emitter.emit_page(stream, page)


__all__ = [
    'SupportedStreams',
]
