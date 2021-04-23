# Standard libraries
import logging
from typing import (
    Iterator,
    Union,
)

# Third party libraries
from returns.curry import partial
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
from tap_delighted.api import (
    ApiClient,
    ApiPage,
    ImpApiPage,
    SurveyPage,
)
from tap_delighted.streams import (
    emitter,
)
from tap_delighted.streams.objs import (
    SupportedStreams,
)


LOG = logging.getLogger(__name__)
ALL = AllPages()


def _stream_data_2(
    stream: SupportedStreams,
    pages: Iterator[IO[ApiPage]],
) -> None:
    for page in pages:
        emitter.emit_iopage(stream, page)


def _stream_data(
    stream: SupportedStreams,
    pages: Iterator[ImpApiPage],
) -> None:
    for page in pages:
        emitter.emit_imp_page(stream, page)


def all_surveys(api: ApiClient) -> None:

    def getter(page: PageId) -> Union[SurveyPage, EmptyPage]:
        result = api.survey.get_surveys(page)
        LOG.debug('get_surveys response: %s', result)
        if result.data.map(bool) == IO(False):
            return EmptyPage()
        return result
    pages: Iterator[SurveyPage] = paginator.get_until_end(
        SurveyPage, PageId(1, 100), getter, 10
    )
    _stream_data(
        SupportedStreams.SURVEY_RESPONSE,
        pages
    )


def all_bounced(api: ApiClient) -> None:
    _stream_data(
        SupportedStreams.BOUNCED,
        api.people.list_bounced(ALL)
    )


def all_metrics(api: ApiClient) -> None:
    stream = SupportedStreams.METRICS
    metrics_io = api.metrics.get_metrics()
    metrics_io.data.map(
        lambda data: emitter.emit_records(stream, iter([data]))
    )


def all_people(api: ApiClient) -> None:
    stream = SupportedStreams.PEOPLE
    data = api.people.list_people()
    data.map(
        partial(emitter.emit_records, stream)
    )


def all_unsubscribed(api: ApiClient) -> None:
    _stream_data(
        SupportedStreams.UNSUBSCRIBED,
        api.people.list_unsubscribed(ALL)
    )


__all__ = [
    'SupportedStreams'
]
