from tap_mailchimp.api.common import (
    api_data,
)
from tap_mailchimp.api.common.api_data import (
    ApiData,
)
from tap_mailchimp.api.common.raw import (
    CampaignId,
    FeedbackId,
    RawSource,
)


def get_campaign(
    raw_source: RawSource,
    campaign: CampaignId,
) -> ApiData:
    return api_data.create_api_data(raw_source.get_campaign(campaign))


def get_feedback(
    raw_source: RawSource,
    feedback_id: FeedbackId,
) -> ApiData:
    return api_data.create_api_data(raw_source.get_feedback(feedback_id))


def get_checklist(
    raw_source: RawSource,
    campaign: CampaignId,
) -> ApiData:
    return api_data.create_api_data(raw_source.get_checklist(campaign))
