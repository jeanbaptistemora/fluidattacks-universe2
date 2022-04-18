import logging
from mailchimp_marketing import (
    Client,
)
from paginator import (
    PageId,
)
from ratelimiter import (
    RateLimiter,
)
from returns.curry import (
    partial,
)
from singer_io.singer2.json import (
    JsonFactory,
    JsonObj,
)
from typing import (
    Callable,
    NamedTuple,
    Union,
)

LOG = logging.getLogger(__name__)


class AudienceId(NamedTuple):
    item_id: str


class AbsReportId(NamedTuple):
    audience_id: AudienceId
    item_id: int


class CampaignId(NamedTuple):
    item_id: str


class FeedbackId(NamedTuple):
    campaign_id: CampaignId
    item_id: int


class GrowthHistId(NamedTuple):
    audience_id: AudienceId
    month: str


class InterestCatgId(NamedTuple):
    audience_id: AudienceId
    item_id: str


class MemberId(NamedTuple):
    audience_id: AudienceId
    item_id: str


ItemId = Union[
    AudienceId,
    AbsReportId,
    CampaignId,
    FeedbackId,
    GrowthHistId,
    InterestCatgId,
    MemberId,
]


class RawSource(NamedTuple):
    list_audiences: Callable[[PageId], JsonObj]
    get_audience: Callable[[AudienceId], JsonObj]
    list_abuse_reports: Callable[[AudienceId, PageId], JsonObj]
    get_abuse_report: Callable[[AbsReportId], JsonObj]
    get_activity: Callable[[AudienceId], JsonObj]
    get_top_clients: Callable[[AudienceId], JsonObj]
    list_members: Callable[[AudienceId, PageId], JsonObj]
    get_member: Callable[[MemberId], JsonObj]
    list_growth_hist: Callable[[AudienceId, PageId], JsonObj]
    get_growth_hist: Callable[[GrowthHistId], JsonObj]
    list_interest_catg: Callable[[AudienceId, PageId], JsonObj]
    get_interest_catg: Callable[[InterestCatgId], JsonObj]
    get_audience_locations: Callable[[AudienceId], JsonObj]
    list_campaigns: Callable[[PageId], JsonObj]
    get_campaign: Callable[[CampaignId], JsonObj]
    list_feedbacks: Callable[[CampaignId], JsonObj]
    get_feedback: Callable[[FeedbackId], JsonObj]
    get_checklist: Callable[[CampaignId], JsonObj]


@RateLimiter(max_calls=5, period=1)
def _list_audiences(client: Client, page_id: PageId) -> JsonObj:
    raw = client.lists.get_all_lists(
        fields=["lists.id", "total_items", "_links"],
        count=page_id.per_page,
        offset=page_id.page * page_id.per_page,
    )
    result = JsonFactory.from_any(raw)
    LOG.debug("_list_audiences (%s) response: %s", page_id, result)
    return result


@RateLimiter(max_calls=5, period=1)
def _get_audience(client: Client, audience_id: AudienceId) -> JsonObj:
    return JsonFactory.from_any(client.lists.get_list(audience_id.item_id))


@RateLimiter(max_calls=5, period=1)
def _list_abuse_reports(
    client: Client, audience_id: AudienceId, page_id: PageId
) -> JsonObj:
    raw = client.lists.get_list_abuse_reports(
        audience_id.item_id,
        fields=["abuse_reports.id", "total_items", "_links"],
        count=page_id.per_page,
        offset=page_id.page * page_id.per_page,
    )
    result = JsonFactory.from_any(raw)
    LOG.debug("_list_abuse_reports response: %s", str(result)[:200])
    return result


@RateLimiter(max_calls=5, period=1)
def _get_abuse_report(client: Client, report_id: AbsReportId) -> JsonObj:
    raw = client.lists.get_list_abuse_report_details(
        report_id.audience_id.item_id, report_id.item_id
    )
    return JsonFactory.from_any(raw)


@RateLimiter(max_calls=5, period=1)
def _get_activity(client: Client, audience_id: AudienceId) -> JsonObj:
    raw = client.lists.get_list_recent_activity(audience_id.item_id)
    return JsonFactory.from_any(raw)


@RateLimiter(max_calls=5, period=1)
def _get_clients(client: Client, audience_id: AudienceId) -> JsonObj:
    return JsonFactory.from_any(
        client.lists.get_list_clients(audience_id.item_id)
    )


@RateLimiter(max_calls=5, period=1)
def _list_members(
    client: Client, audience_id: AudienceId, page_id: PageId
) -> JsonObj:
    raw = client.lists.get_list_members_info(
        audience_id.item_id,
        fields=["members.id", "total_items", "_links"],
        count=page_id.per_page,
        offset=page_id.page * page_id.per_page,
    )
    result = JsonFactory.from_any(raw)
    LOG.debug(
        "_list_members(%s, %s) response: %s",
        audience_id,
        page_id,
        str(result)[:200],
    )
    return result


@RateLimiter(max_calls=5, period=1)
def _get_member(client: Client, member_id: MemberId) -> JsonObj:
    raw = client.lists.get_list_member(
        member_id.audience_id.item_id,
        member_id.item_id,
        exclude_fields=["tags"],
    )
    result = JsonFactory.from_any(raw)
    return result


@RateLimiter(max_calls=5, period=1)
def _list_growth_hist(
    client: Client, audience_id: AudienceId, page_id: PageId
) -> JsonObj:
    raw = client.lists.get_list_growth_history(
        audience_id.item_id,
        fields=["history.month", "total_items", "_links"],
        count=page_id.per_page,
        offset=page_id.page * page_id.per_page,
    )
    result = JsonFactory.from_any(raw)
    return result


@RateLimiter(max_calls=5, period=1)
def _get_growth_hist(client: Client, ghist_id: GrowthHistId) -> JsonObj:
    raw = client.lists.get_list_growth_history_by_month(
        ghist_id.audience_id.item_id, ghist_id.month
    )
    return JsonFactory.from_any(raw)


@RateLimiter(max_calls=5, period=1)
def _list_interest_catg(
    client: Client, audience_id: AudienceId, page_id: PageId
) -> JsonObj:
    raw = client.lists.get_list_interest_categories(
        audience_id.item_id,
        fields=["categories.id", "total_items", "_links"],
        count=page_id.per_page,
        offset=page_id.page * page_id.per_page,
    )
    return JsonFactory.from_any(raw)


@RateLimiter(max_calls=5, period=1)
def _get_interest_catg(client: Client, interest_id: InterestCatgId) -> JsonObj:
    raw = client.lists.get_interest_category(
        interest_id.audience_id.item_id, interest_id.item_id
    )
    return JsonFactory.from_any(raw)


@RateLimiter(max_calls=5, period=1)
def _get_audience_locations(
    client: Client, audience_id: AudienceId
) -> JsonObj:
    return JsonFactory.from_any(
        client.lists.get_list_locations(audience_id.item_id)
    )


@RateLimiter(max_calls=5, period=1)
def _list_campaigns(client: Client, page_id: PageId) -> JsonObj:
    raw = client.campaigns.list(
        fields=["campaigns.id", "total_items", "_links"],
        count=page_id.per_page,
        offset=page_id.page * page_id.per_page,
    )
    result = JsonFactory.from_any(raw)
    LOG.debug("_list_campaigns response: %s", result)
    return result


@RateLimiter(max_calls=5, period=1)
def _get_campaign(client: Client, campaign_id: CampaignId) -> JsonObj:
    return JsonFactory.from_any(client.campaigns.get(campaign_id.item_id))


@RateLimiter(max_calls=5, period=1)
def _list_feedbacks(client: Client, campaign_id: CampaignId) -> JsonObj:
    raw = client.campaigns.get_feedback(
        campaign_id.item_id,
        fields=["feedback.feedback_id", "total_items", "_links"],
    )
    result = JsonFactory.from_any(raw)
    LOG.debug("_list_feedbacks response: %s", result)
    return result


@RateLimiter(max_calls=5, period=1)
def _get_feedback(client: Client, feedback_id: FeedbackId) -> JsonObj:
    raw = client.campaigns.get_feedback_message(
        feedback_id.campaign_id.item_id,
        feedback_id.item_id,
    )
    return JsonFactory.from_any(raw)


@RateLimiter(max_calls=5, period=1)
def _get_checklist(client: Client, campaign_id: CampaignId) -> JsonObj:
    LOG.info("getting %s", campaign_id)
    raw = client.campaigns.get_send_checklist(campaign_id.item_id)
    LOG.info("done %s", campaign_id)
    return JsonFactory.from_any(raw)


def create_raw_source(client: Client) -> RawSource:
    return RawSource(
        list_audiences=partial(_list_audiences, client),
        get_audience=partial(_get_audience, client),
        list_abuse_reports=partial(_list_abuse_reports, client),
        get_abuse_report=partial(_get_abuse_report, client),
        get_activity=partial(_get_activity, client),
        get_top_clients=partial(_get_clients, client),
        list_members=partial(_list_members, client),
        get_member=partial(_get_member, client),
        list_growth_hist=partial(_list_growth_hist, client),
        get_growth_hist=partial(_get_growth_hist, client),
        list_interest_catg=partial(_list_interest_catg, client),
        get_interest_catg=partial(_get_interest_catg, client),
        get_audience_locations=partial(_get_audience_locations, client),
        list_campaigns=partial(_list_campaigns, client),
        get_campaign=partial(_get_campaign, client),
        list_feedbacks=partial(_list_feedbacks, client),
        get_feedback=partial(_get_feedback, client),
        get_checklist=partial(_get_checklist, client),
    )
