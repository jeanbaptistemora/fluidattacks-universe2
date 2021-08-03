from functools import (
    partial,
)
import logging
from singer_io.singer2.json import (
    JsonObj,
)
from tap_mailchimp.api.common import (
    list_items,
    list_unsupported_pagination,
)
from tap_mailchimp.api.common.raw import (
    CampaignId,
    FeedbackId,
    RawSource,
)
from typing import (
    Iterator,
)

LOG = logging.getLogger(__name__)


def list_campaigns(
    raw_source: RawSource,
) -> Iterator[CampaignId]:
    def id_builder(item: JsonObj) -> CampaignId:
        return CampaignId(item["id"].to_primitive(str))

    return list_items(raw_source.list_campaigns, "campaigns", id_builder)


def list_feedbacks(
    raw_source: RawSource,
    campaign_id: CampaignId,
) -> Iterator[FeedbackId]:
    def id_builder(item: JsonObj) -> FeedbackId:
        return FeedbackId(campaign_id, item["feedback_id"].to_primitive(int))

    return list_unsupported_pagination(
        partial(raw_source.list_feedbacks, campaign_id), "feedback", id_builder
    )
