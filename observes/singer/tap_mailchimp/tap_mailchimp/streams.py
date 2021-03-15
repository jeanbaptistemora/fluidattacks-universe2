# Standard libraries
import sys
from collections import (
    deque,
)
from enum import Enum
from itertools import (
    chain,
)
from typing import (
    Any,
    Callable,
    IO,
    Iterator,
    Mapping,
    Optional,
)

# Third party libraries

# Local libraries
from singer_io import factory
from singer_io.singer import (
    SingerRecord,
)
from tap_mailchimp.api import (
    AbsReportId,
    ApiClient,
    ApiData,
    AudienceId,
    ItemId,
)


class SupportedStreams(Enum):
    AUDIENCES = 'AUDIENCES'
    ABUSE_REPORTS = 'ABUSE_REPORTS'


def _item_getter(
    client: ApiClient,
    stream: SupportedStreams,
    item_id: ItemId
) -> ApiData:
    getter: Mapping[
        SupportedStreams,
        Callable[[Any], ApiData]
    ] = {
        SupportedStreams.AUDIENCES: client.get_audience,
        SupportedStreams.ABUSE_REPORTS: client.get_abuse_report
    }
    id_type = {
        SupportedStreams.AUDIENCES: AudienceId,
        SupportedStreams.ABUSE_REPORTS: AbsReportId
    }
    assert isinstance(item_id, id_type[stream])
    return getter[stream](item_id)


def _emit_item(
    client: ApiClient,
    stream: SupportedStreams,
    item_id: ItemId,
    target: Optional[IO[str]]
) -> None:
    target = target if target else sys.stdout
    result = _item_getter(client, stream, item_id)
    record = SingerRecord(
        stream=stream.value.lower(),
        record=result.data
    )
    factory.emit(record, target)


def _emit_items(
    client: ApiClient,
    stream: SupportedStreams,
    items_id: Iterator[ItemId],
    target: Optional[IO[str]]
) -> None:
    first_item = next(items_id, None)
    if not first_item:
        return
    _emit_item(client, stream, first_item, target)
    map_obj = map(
        lambda id: _emit_item(client, stream, id, target),
        items_id
    )
    deque(map_obj, 0)


def _get_audiences_id(client: ApiClient) -> Iterator[AudienceId]:
    audiences_data = client.list_audiences().data['lists']
    return iter(map(lambda a: AudienceId(a['id']), audiences_data))


def _get_reports_id(
    client: ApiClient,
    audience: AudienceId
) -> Iterator[AbsReportId]:
    data = client.list_abuse_reports(audience).data['abuse_reports']
    return iter(map(
        lambda item: AbsReportId(
            audience_id=audience,
            str_id=item['id']
        ),
        data
    ))


def all_audiences(client: ApiClient, target: Optional[IO[str]]) -> None:
    stream = SupportedStreams.AUDIENCES
    audiences_id = _get_audiences_id(client)
    if audiences_id:
        _emit_items(client, stream, audiences_id, target)


def all_abuse_reports(client: ApiClient, target: Optional[IO[str]]) -> None:
    stream = SupportedStreams.ABUSE_REPORTS
    audiences_id = _get_audiences_id(client)
    reports_id: Iterator[AbsReportId] = chain.from_iterable(iter(map(
        lambda audience: _get_reports_id(client, audience),
        audiences_id
    )))
    _emit_items(client, stream, reports_id, target)


stream_executor: Mapping[
    SupportedStreams,
    Callable[[ApiClient, Optional[IO[str]]], None]
] = {
    SupportedStreams.AUDIENCES: all_audiences
}
