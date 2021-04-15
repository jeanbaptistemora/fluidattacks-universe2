# Standard libraries
import logging
from typing import (
    Iterator,
    TypeVar,
    Union,
)

# Third party libraries
from returns.curry import (
    partial,
)
from returns.io import (
    IO,
)

# Local libraries
import paginator
from paginator import (
    AllPages,
    EmptyPage,
    PageId,
)
from singer_io import (
    factory,
)
from singer_io.singer import (
    SingerRecord,
)
from tap_delighted.api import (
    ApiClient,
    SurveyPage,
    BouncedPage,
    UnsubscribedPage,
)
from tap_delighted.common import (
    JSON,
)
from tap_delighted.streams.objs import (
    SupportedStreams,
)


LOG = logging.getLogger(__name__)
ApiPage = TypeVar('ApiPage', SurveyPage, BouncedPage, UnsubscribedPage)


def _json_list_srecords(
    stream: str,
    items: Iterator[JSON]
) -> Iterator[SingerRecord]:
    return iter(map(
        lambda item: SingerRecord(
            stream=stream,
            record=item
        ),
        items
    ))


def _emit_records(records: Iterator[SingerRecord]) -> None:
    for record in records:
        factory.emit(record)


def _emit_page(stream: SupportedStreams, page: ApiPage) -> None:
    records: IO[Iterator[SingerRecord]] = page.data.map(
        partial(_json_list_srecords, stream.value.lower())
    )
    records.map(_emit_records)


def all_surveys(api: ApiClient) -> None:
    stream = SupportedStreams.SURVEY_RESPONSE

    def getter(page: PageId) -> Union[SurveyPage, EmptyPage]:
        result = api.survey.get_surveys(page)
        LOG.debug('get_surveys response: %s', result)
        if result.data.map(bool) == IO(False):
            return EmptyPage()
        return result
    pages: Iterator[SurveyPage] = paginator.get_until_end(
        PageId(1, 100), getter, 10
    )
    for page in pages:
        _emit_page(stream, page)


def all_bounced(api: ApiClient) -> None:
    stream = SupportedStreams.BOUNCED
    pages = api.people.list_bounced(AllPages())
    for page in pages:
        _emit_page(stream, page)


def all_unsubscribed(api: ApiClient) -> None:
    stream = SupportedStreams.UNSUBSCRIBED
    pages = api.people.list_unsubscribed(AllPages())
    for page in pages:
        _emit_page(stream, page)


def all_metrics(api: ApiClient) -> None:
    stream = SupportedStreams.METRICS
    metrics = api.metrics.get_metrics()
    records: IO[Iterator[SingerRecord]] = metrics.data.map(
        lambda data: partial(
            _json_list_srecords, stream.value.lower()
        )(iter([data]))
    )
    records.map(_emit_records)


__all__ = [
    'SupportedStreams'
]
