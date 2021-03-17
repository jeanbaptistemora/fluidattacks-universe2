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
    Union,
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
    GrowthHistId,
    ItemId,
    MemberId,
)


class SupportedStreams(Enum):
    AUDIENCES = 'AUDIENCES'
    ABUSE_REPORTS = 'ABUSE_REPORTS'
    MEMBERS = 'MEMBERS'
    RECENT_ACTIVITY = 'RECENT_ACTIVITY'
    TOP_CLIENTS = 'TOP_CLIENTS'
    GROWTH_HISTORY = 'GROWTH_HISTORY'


def _item_getter(
    client: ApiClient,
    stream: SupportedStreams,
    item_id: ItemId
) -> Union[ApiData, Iterator[ApiData]]:
    getter: Mapping[
        SupportedStreams,
        Callable[[Any], Any],
    ] = {
        SupportedStreams.AUDIENCES: client.get_audience,
        SupportedStreams.ABUSE_REPORTS: client.get_abuse_report,
        SupportedStreams.RECENT_ACTIVITY: client.get_activity,
        SupportedStreams.TOP_CLIENTS: client.get_top_clients,
        SupportedStreams.MEMBERS: client.get_member,
        SupportedStreams.GROWTH_HISTORY: client.get_growth_hist,
    }
    id_type = {
        SupportedStreams.AUDIENCES: AudienceId,
        SupportedStreams.ABUSE_REPORTS: AbsReportId,
        SupportedStreams.RECENT_ACTIVITY: AudienceId,
        SupportedStreams.TOP_CLIENTS: AudienceId,
        SupportedStreams.MEMBERS: MemberId,
        SupportedStreams.GROWTH_HISTORY: GrowthHistId,
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
    results = _item_getter(client, stream, item_id)
    if isinstance(results, ApiData):
        results = iter([results])
    for result in results:
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


def all_audiences(client: ApiClient, target: Optional[IO[str]]) -> None:
    stream = SupportedStreams.AUDIENCES
    audiences_id = client.list_audiences()
    _emit_items(client, stream, audiences_id, target)


def all_abuse_reports(client: ApiClient, target: Optional[IO[str]]) -> None:
    stream = SupportedStreams.ABUSE_REPORTS
    audiences_id = client.list_audiences()
    reports_id: Iterator[AbsReportId] = chain.from_iterable(iter(map(
        client.list_abuse_reports,
        audiences_id
    )))
    _emit_items(client, stream, reports_id, target)


def all_growth_history(client: ApiClient, target: Optional[IO[str]]) -> None:
    stream = SupportedStreams.GROWTH_HISTORY
    audiences_id = client.list_audiences()
    histories_id: Iterator[GrowthHistId] = chain.from_iterable(iter(map(
        client.list_growth_hist,
        audiences_id
    )))
    _emit_items(client, stream, histories_id, target)


def all_members(client: ApiClient, target: Optional[IO[str]]) -> None:
    stream = SupportedStreams.MEMBERS
    audiences_id = client.list_audiences()
    members_id: Iterator[MemberId] = chain.from_iterable(iter(map(
        client.list_members,
        audiences_id
    )))
    _emit_items(client, stream, members_id, target)


def recent_activity(client: ApiClient, target: Optional[IO[str]]) -> None:
    stream = SupportedStreams.RECENT_ACTIVITY
    audiences_id = client.list_audiences()
    _emit_items(client, stream, audiences_id, target)


def top_clients(client: ApiClient, target: Optional[IO[str]]) -> None:
    stream = SupportedStreams.TOP_CLIENTS
    audiences_id = client.list_audiences()
    _emit_items(client, stream, audiences_id, target)
