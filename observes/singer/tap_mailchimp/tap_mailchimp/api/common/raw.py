# Standard libraries
import logging
from functools import (
    partial,
)
from typing import (
    Callable,
    NamedTuple,
    Union,
)

# Third party libraries
from mailchimp_marketing import (
    Client,
)
from ratelimiter import RateLimiter

# Local libraries
from paginator import (
    PageId,
)
from tap_mailchimp.common.objs import (
    JSON,
)


LOG = logging.getLogger(__name__)


class AudienceId(NamedTuple):
    str_id: str


class AbsReportId(NamedTuple):
    audience_id: AudienceId
    str_id: str


class CampaignId(NamedTuple):
    str_id: str


class FeedbackId(NamedTuple):
    campaign_id: CampaignId
    str_id: str


class GrowthHistId(NamedTuple):
    audience_id: AudienceId
    str_id: str


class InterestCatgId(NamedTuple):
    audience_id: AudienceId
    str_id: str


class MemberId(NamedTuple):
    audience_id: AudienceId
    str_id: str


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
    list_audiences: Callable[[PageId], JSON]
    get_audience: Callable[[AudienceId], JSON]
    list_abuse_reports: Callable[[AudienceId, PageId], JSON]
    get_abuse_report: Callable[[AbsReportId], JSON]
    get_activity: Callable[[AudienceId], JSON]
    get_top_clients: Callable[[AudienceId], JSON]
    list_members: Callable[[AudienceId, PageId], JSON]
    get_member: Callable[[MemberId], JSON]
    list_growth_hist: Callable[[AudienceId, PageId], JSON]
    get_growth_hist: Callable[[GrowthHistId], JSON]
    list_interest_catg: Callable[[AudienceId, PageId], JSON]
    get_interest_catg: Callable[[InterestCatgId], JSON]
    get_audience_locations: Callable[[AudienceId], JSON]
    list_campaigns: Callable[[PageId], JSON]
    get_campaign: Callable[[CampaignId], JSON]
    list_feedbacks: Callable[[CampaignId, PageId], JSON]
    get_feedback: Callable[[FeedbackId], JSON]
    get_checklist: Callable[[CampaignId], JSON]


@RateLimiter(max_calls=5, period=1)
def _list_audiences(client: Client, page_id: PageId) -> JSON:
    result = client.lists.get_all_lists(
        fields=['lists.id', 'total_items', '_links'],
        count=page_id.per_page,
        offset=page_id.page * page_id.per_page
    )
    LOG.debug('_list_audiences (%s) response: %s', page_id, result)
    return result


@RateLimiter(max_calls=5, period=1)
def _get_audience(client: Client, audience_id: AudienceId) -> JSON:
    return client.lists.get_list(audience_id.str_id)


@RateLimiter(max_calls=5, period=1)
def _list_abuse_reports(
    client: Client, audience_id: AudienceId, page_id: PageId
) -> JSON:
    result = client.lists.get_list_abuse_reports(
        audience_id.str_id,
        fields=['abuse_reports.id', 'total_items', '_links'],
        count=page_id.per_page,
        offset=page_id.page * page_id.per_page
    )
    LOG.debug('_list_abuse_reports response: %s', str(result)[:200])
    return result


@RateLimiter(max_calls=5, period=1)
def _get_abuse_report(client: Client, report_id: AbsReportId) -> JSON:
    return client.lists.get_list_abuse_report_details(
        report_id.audience_id.str_id, report_id.str_id
    )


@RateLimiter(max_calls=5, period=1)
def _get_activity(client: Client, audience_id: AudienceId) -> JSON:
    return client.lists.get_list_recent_activity(audience_id.str_id)


@RateLimiter(max_calls=5, period=1)
def _get_clients(client: Client, audience_id: AudienceId) -> JSON:
    return client.lists.get_list_clients(audience_id.str_id)


@RateLimiter(max_calls=5, period=1)
def _list_members(
    client: Client, audience_id: AudienceId, page_id: PageId
) -> JSON:
    result = client.lists.get_list_members_info(
        audience_id.str_id,
        fields=['members.id', 'total_items', '_links'],
        count=page_id.per_page,
        offset=page_id.page * page_id.per_page
    )
    LOG.debug(
        '_list_members(%s, %s) response: %s',
        audience_id, page_id, str(result)[:200]
    )
    return result


@RateLimiter(max_calls=5, period=1)
def _get_member(client: Client, member_id: MemberId) -> JSON:
    result = client.lists.get_list_member(
        member_id.audience_id.str_id,
        member_id.str_id,
        exclude_fields=['tags']
    )
    LOG.debug('_get_member(%s) response: %s', member_id, result)
    return result


@RateLimiter(max_calls=5, period=1)
def _list_growth_hist(
    client: Client, audience_id: AudienceId, page_id: PageId
) -> JSON:
    return client.lists.get_list_growth_history(
        audience_id.str_id,
        fields=['history.month', 'total_items', '_links'],
        count=page_id.per_page,
        offset=page_id.page * page_id.per_page
    )


@RateLimiter(max_calls=5, period=1)
def _get_growth_hist(client: Client, ghist_id: GrowthHistId) -> JSON:
    return client.lists.get_list_growth_history_by_month(
        ghist_id.audience_id.str_id,
        ghist_id.str_id
    )


@RateLimiter(max_calls=5, period=1)
def _list_interest_catg(
    client: Client, audience_id: AudienceId, page_id: PageId
) -> JSON:
    return client.lists.get_list_interest_categories(
        audience_id.str_id,
        fields=['categories.id', 'total_items', '_links'],
        count=page_id.per_page,
        offset=page_id.page * page_id.per_page
    )


@RateLimiter(max_calls=5, period=1)
def _get_interest_catg(client: Client, interest_id: InterestCatgId) -> JSON:
    return client.lists.get_interest_category(
        interest_id.audience_id.str_id,
        interest_id.str_id
    )


@RateLimiter(max_calls=5, period=1)
def _get_audience_locations(client: Client, audience_id: AudienceId) -> JSON:
    return client.lists.get_list_locations(audience_id.str_id)


@RateLimiter(max_calls=5, period=1)
def _list_campaigns(client: Client, page_id: PageId) -> JSON:
    result = client.campaigns.list(
        fields=['campaigns.id', 'total_items', '_links'],
        count=page_id.per_page,
        offset=page_id.page * page_id.per_page
    )
    LOG.debug('_list_campaigns response: %s', result)
    return result


@RateLimiter(max_calls=5, period=1)
def _get_campaign(client: Client, campaign_id: CampaignId) -> JSON:
    return client.campaigns.get(campaign_id.str_id)


@RateLimiter(max_calls=5, period=1)
def _list_feedbacks(
    client: Client, campaign_id: CampaignId, page_id: PageId
) -> JSON:
    return client.campaigns.get_feedback(
        campaign_id.str_id,
        fields=['feedback.feedback_id', 'total_items', '_links'],
        count=page_id.per_page,
        offset=page_id.page * page_id.per_page
    )


@RateLimiter(max_calls=5, period=1)
def _get_feedback(client: Client, feedback_id: FeedbackId) -> JSON:
    return client.campaigns.get_feedback_message(
        feedback_id.campaign_id.str_id,
        feedback_id.str_id,
    )


@RateLimiter(max_calls=5, period=1)
def _get_checklist(
    client: Client, campaign_id: CampaignId
) -> JSON:
    return client.campaigns.get_send_checklist(campaign_id.str_id)


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
