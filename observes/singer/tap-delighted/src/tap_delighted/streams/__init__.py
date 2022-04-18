import logging
from paginator import (
    AllPages,
)
from returns.curry import (
    partial,
)
from returns.io import (
    IO,
)
from tap_delighted.api import (
    ApiClient,
    ApiPage,
)
from tap_delighted.streams import (
    emitter,
)
from tap_delighted.streams.objs import (
    SupportedStreams,
)
from typing import (
    Iterator,
)

LOG = logging.getLogger(__name__)
ALL = AllPages()


def _stream_data(
    stream: SupportedStreams,
    pages: Iterator[IO[ApiPage]],
) -> None:
    for page in pages:
        emitter.emit_iopage(stream, page)


def all_surveys(api: ApiClient) -> None:
    _stream_data(
        SupportedStreams.SURVEY_RESPONSE, api.survey.list_surveys(ALL)
    )


def all_bounced(api: ApiClient) -> None:
    _stream_data(SupportedStreams.BOUNCED, api.people.list_bounced(ALL))


def all_metrics(api: ApiClient) -> None:
    stream = SupportedStreams.METRICS
    metrics_io = api.metrics.get_metrics()
    metrics_io.map(
        lambda metrics: emitter.emit_records(stream, iter([metrics.data]))
    )


def all_people(api: ApiClient) -> None:
    stream = SupportedStreams.PEOPLE
    data = api.people.list_people()
    data.map(partial(emitter.emit_records, stream))


def all_unsubscribed(api: ApiClient) -> None:
    _stream_data(
        SupportedStreams.UNSUBSCRIBED, api.people.list_unsubscribed(ALL)
    )


__all__ = ["SupportedStreams"]
