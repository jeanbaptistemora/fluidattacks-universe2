from collections import (
    deque,
)
from enum import (
    Enum,
)
from itertools import (
    chain,
)
from singer_io.singer2 import (
    SingerEmitter,
    SingerRecord,
)
from singer_io.singer2.json import (
    JsonEmitter,
)
import sys
from tap_mailchimp.api import (
    AbsReportId,
    ApiClient,
    ApiData,
    AudienceId,
    CampaignId,
    FeedbackId,
    GrowthHistId,
    InterestCatgId,
    ItemId,
    MemberId,
)
from typing import (
    Any,
    Callable,
    cast,
    IO,
    Iterator,
    Mapping,
    Optional,
    Union,
)


class SupportedStreams(Enum):
    AUDIENCES = "AUDIENCES"
    ABUSE_REPORTS = "ABUSE_REPORTS"
    CAMPAIGNS = "CAMPAIGNS"
    CHECKLIST = "CHECKLIST"
    FEEDBACK = "FEEDBACK"
    GROWTH_HISTORY = "GROWTH_HISTORY"
    INTEREST_CATEGORY = "INTEREST_CATEGORY"
    LOCATIONS = "LOCATIONS"
    MEMBERS = "MEMBERS"
    RECENT_ACTIVITY = "RECENT_ACTIVITY"
    TOP_CLIENTS = "TOP_CLIENTS"


def _item_getter(
    client: ApiClient, stream: SupportedStreams, item_id: ItemId
) -> Union[ApiData, Iterator[ApiData]]:
    getter: Mapping[SupportedStreams, Callable[[Any], Any]] = {
        SupportedStreams.AUDIENCES: client.get_audience,
        SupportedStreams.ABUSE_REPORTS: client.get_abuse_report,
        SupportedStreams.GROWTH_HISTORY: client.get_growth_hist,
        SupportedStreams.INTEREST_CATEGORY: client.get_interest_catg,
        SupportedStreams.LOCATIONS: client.get_audience_locations,
        SupportedStreams.MEMBERS: client.get_member,
        SupportedStreams.RECENT_ACTIVITY: client.get_activity,
        SupportedStreams.TOP_CLIENTS: client.get_top_clients,
        SupportedStreams.CAMPAIGNS: client.get_campaign,
        SupportedStreams.CHECKLIST: client.get_checklist,
        SupportedStreams.FEEDBACK: client.get_feedback,
    }
    id_type = {
        SupportedStreams.AUDIENCES: AudienceId,
        SupportedStreams.ABUSE_REPORTS: AbsReportId,
        SupportedStreams.GROWTH_HISTORY: GrowthHistId,
        SupportedStreams.INTEREST_CATEGORY: InterestCatgId,
        SupportedStreams.LOCATIONS: AudienceId,
        SupportedStreams.MEMBERS: MemberId,
        SupportedStreams.RECENT_ACTIVITY: AudienceId,
        SupportedStreams.TOP_CLIENTS: AudienceId,
        SupportedStreams.CAMPAIGNS: CampaignId,
        SupportedStreams.CHECKLIST: CampaignId,
        SupportedStreams.FEEDBACK: FeedbackId,
    }
    if isinstance(item_id, id_type[stream]):
        return getter[stream](item_id)
    raise TypeError(
        f"Expected type `{id_type[stream]}` but recieved `{type(item_id)}`"
    )


def _emit_item(
    client: ApiClient,
    stream: SupportedStreams,
    item_id: ItemId,
    target: Optional[IO[str]],
) -> None:
    target = target if target else sys.stdout
    results = _item_getter(client, stream, item_id)
    emitter = SingerEmitter(JsonEmitter(target))
    if isinstance(results, ApiData):
        results = iter([results])
    for result in results:
        record = SingerRecord(stream=stream.value.lower(), record=result.data)
        emitter.emit(record)


def _emit_items(
    client: ApiClient,
    stream: SupportedStreams,
    items_id: Iterator[ItemId],
    target: Optional[IO[str]],
) -> None:
    first_item: Optional[ItemId] = next(items_id, None)
    if first_item is None:
        return
    _emit_item(client, stream, cast(ItemId, first_item), target)
    map_obj = map(lambda id: _emit_item(client, stream, id, target), items_id)
    deque(map_obj, 0)


def all_audiences(client: ApiClient, target: Optional[IO[str]]) -> None:
    stream = SupportedStreams.AUDIENCES
    audiences_id = client.list_audiences()
    _emit_items(client, stream, audiences_id, target)


def all_abuse_reports(client: ApiClient, target: Optional[IO[str]]) -> None:
    stream = SupportedStreams.ABUSE_REPORTS
    audiences_id = client.list_audiences()
    reports_id: Iterator[AbsReportId] = chain.from_iterable(
        iter(map(client.list_abuse_reports, audiences_id))
    )
    _emit_items(client, stream, reports_id, target)


def all_growth_history(client: ApiClient, target: Optional[IO[str]]) -> None:
    stream = SupportedStreams.GROWTH_HISTORY
    audiences_id = client.list_audiences()
    histories_id: Iterator[GrowthHistId] = chain.from_iterable(
        iter(map(client.list_growth_hist, audiences_id))
    )
    _emit_items(client, stream, histories_id, target)


def all_members(client: ApiClient, target: Optional[IO[str]]) -> None:
    stream = SupportedStreams.MEMBERS
    audiences_id = client.list_audiences()
    members_id: Iterator[MemberId] = chain.from_iterable(
        iter(map(client.list_members, audiences_id))
    )
    _emit_items(client, stream, members_id, target)


def recent_activity(client: ApiClient, target: Optional[IO[str]]) -> None:
    stream = SupportedStreams.RECENT_ACTIVITY
    audiences_id = client.list_audiences()
    _emit_items(client, stream, audiences_id, target)


def top_clients(client: ApiClient, target: Optional[IO[str]]) -> None:
    stream = SupportedStreams.TOP_CLIENTS
    audiences_id = client.list_audiences()
    _emit_items(client, stream, audiences_id, target)


def all_interest_category(
    client: ApiClient, target: Optional[IO[str]]
) -> None:
    stream = SupportedStreams.INTEREST_CATEGORY
    audiences_id = client.list_audiences()
    interest_catgs_id: Iterator[InterestCatgId] = chain.from_iterable(
        iter(map(client.list_interest_catg, audiences_id))
    )
    _emit_items(client, stream, interest_catgs_id, target)


def all_locations(client: ApiClient, target: Optional[IO[str]]) -> None:
    stream = SupportedStreams.LOCATIONS
    audiences_id = client.list_audiences()
    _emit_items(client, stream, audiences_id, target)


def all_campaigns(client: ApiClient, target: Optional[IO[str]]) -> None:
    stream = SupportedStreams.CAMPAIGNS
    campaigns_id = client.list_campaigns()
    _emit_items(client, stream, campaigns_id, target)


def all_checklists(client: ApiClient, target: Optional[IO[str]]) -> None:
    stream = SupportedStreams.CHECKLIST
    campaigns_id = client.list_campaigns()
    _emit_items(client, stream, campaigns_id, target)


def all_feedback(client: ApiClient, target: Optional[IO[str]]) -> None:
    stream = SupportedStreams.FEEDBACK
    campaigns_id = client.list_campaigns()
    feedbacks_id: Iterator[FeedbackId] = chain.from_iterable(
        iter(map(client.list_feedbacks, campaigns_id))
    )
    _emit_items(client, stream, feedbacks_id, target)
