# Standard libraries
from itertools import (
    chain,
)
from typing import (
    Iterator,
    Union,
)

# Third party libraries
from returns.curry import (
    partial,
)

# Local libraries
import paginator
from paginator import (
    EmptyPage,
    PageId,
)
from tap_delighted.api import ApiClient
from tap_delighted.api.survey import (
    SurveyResponsePage,
)
from tap_delighted.common import (
    JSON,
)
from tap_delighted.streams.objs import (
    SupportedStreams,
)
from singer_io import (
    factory,
)
from singer_io.singer import (
    SingerRecord,
)


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


def all_surveys(api: ApiClient) -> None:
    stream = SupportedStreams.SURVEY_RESPONSE

    def getter(page: PageId) -> Union[SurveyResponsePage, EmptyPage]:
        result = api.survey.get_surveys(page)
        if not result:
            return EmptyPage()
        return result
    pages: Iterator[SurveyResponsePage] = paginator.get_until_end(
        PageId(1, 100), getter, 10
    )
    s_records = chain.from_iterable(map(
        partial(_json_list_srecords, stream.value.lower()),
        map(lambda page: page.data, pages)
    ))
    for record in s_records:
        factory.emit(record)


__all__ = [
    'SupportedStreams'
]
