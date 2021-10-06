from functools import (
    partial,
)
import logging
from mailchimp_marketing import (
    Client,
)
from tap_mailchimp.api import (
    audiences,
    campaigns,
)
from tap_mailchimp.api.common import (
    raw as raw_module,
)
from tap_mailchimp.api.common.api_data import (
    ApiData,
)
from tap_mailchimp.api.common.raw import (
    AbsReportId,
    AudienceId,
    CampaignId,
    FeedbackId,
    GrowthHistId,
    InterestCatgId,
    ItemId,
    MemberId,
    RawSource,
)
from tap_mailchimp.auth import (
    Credentials,
)
from typing import (
    Callable,
    Iterator,
    NamedTuple,
)

LOG = logging.getLogger(__name__)


class ApiClient(NamedTuple):
    list_audiences: Callable[[], Iterator[AudienceId]]
    get_audience: Callable[[AudienceId], ApiData]
    list_abuse_reports: Callable[[AudienceId], Iterator[AbsReportId]]
    get_abuse_report: Callable[[AbsReportId], ApiData]
    get_activity: Callable[[AudienceId], Iterator[ApiData]]
    get_top_clients: Callable[[AudienceId], Iterator[ApiData]]
    list_members: Callable[[AudienceId], Iterator[MemberId]]
    get_member: Callable[[MemberId], ApiData]
    list_growth_hist: Callable[[AudienceId], Iterator[GrowthHistId]]
    get_growth_hist: Callable[[GrowthHistId], ApiData]
    list_interest_catg: Callable[[AudienceId], Iterator[InterestCatgId]]
    get_interest_catg: Callable[[InterestCatgId], ApiData]
    get_audience_locations: Callable[[AudienceId], Iterator[ApiData]]
    list_campaigns: Callable[[], Iterator[CampaignId]]
    get_campaign: Callable[[CampaignId], ApiData]
    list_feedbacks: Callable[[CampaignId], Iterator[FeedbackId]]
    get_feedback: Callable[[FeedbackId], ApiData]
    get_checklist: Callable[[CampaignId], ApiData]


def new_client_from_source(raw_source: RawSource) -> ApiClient:
    return ApiClient(
        list_audiences=partial(
            audiences.list_items.list_audiences, raw_source
        ),
        get_audience=partial(audiences.get_item.get_audience, raw_source),
        list_abuse_reports=partial(
            audiences.list_items.list_abuse_reports, raw_source
        ),
        get_abuse_report=partial(
            audiences.get_item.get_abuse_report, raw_source
        ),
        get_activity=partial(audiences.get_item.get_activity, raw_source),
        get_top_clients=partial(
            audiences.get_item.get_top_clients, raw_source
        ),
        list_members=partial(audiences.list_items.list_members, raw_source),
        get_member=partial(audiences.get_item.get_member, raw_source),
        list_growth_hist=partial(
            audiences.list_items.list_growth_hist, raw_source
        ),
        get_growth_hist=partial(
            audiences.get_item.get_growth_hist, raw_source
        ),
        list_interest_catg=partial(
            audiences.list_items.list_interest_catg, raw_source
        ),
        get_interest_catg=partial(
            audiences.get_item.get_interest_catg, raw_source
        ),
        get_audience_locations=partial(
            audiences.get_item.get_audience_locations, raw_source
        ),
        list_campaigns=partial(
            campaigns.list_items.list_campaigns, raw_source
        ),
        get_campaign=partial(campaigns.get_item.get_campaign, raw_source),
        list_feedbacks=partial(
            campaigns.list_items.list_feedbacks, raw_source
        ),
        get_feedback=partial(campaigns.get_item.get_feedback, raw_source),
        get_checklist=partial(campaigns.get_item.get_checklist, raw_source),
    )


def new_client(creds: Credentials) -> ApiClient:
    client = Client()
    client.set_config({"api_key": creds.api_key, "server": creds.dc})
    raw_source = raw_module.create_raw_source(client)
    return new_client_from_source(raw_source)


# export types
__all__ = [
    "AbsReportId",
    "ApiData",
    "AudienceId",
    "CampaignId",
    "FeedbackId",
    "GrowthHistId",
    "ItemId",
    "InterestCatgId",
    "MemberId",
    "RawSource",
]
