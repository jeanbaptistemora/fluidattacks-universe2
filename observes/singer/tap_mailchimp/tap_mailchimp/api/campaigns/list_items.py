# Standard libraries
import logging
from functools import (
    partial,
)
from typing import (
    Dict,
    Iterator,
)

# Third party libraries

# Local libraries
from tap_mailchimp.api.common import (
    list_items,
    list_unsupported_pagination,
)
from tap_mailchimp.api.common.raw import (
    CampaignId,
    FeedbackId,
    RawSource,
)


LOG = logging.getLogger(__name__)


def list_campaigns(
    raw_source: RawSource,
) -> Iterator[CampaignId]:
    def id_builder(item: Dict[str, str]) -> CampaignId:
        return CampaignId(
            str_id=item['id']
        )

    return list_items(
        raw_source.list_campaigns,
        'campaigns',
        id_builder
    )


def list_feedbacks(
    raw_source: RawSource,
    campaign_id: CampaignId,
) -> Iterator[FeedbackId]:
    def id_builder(item: Dict[str, str]) -> FeedbackId:
        return FeedbackId(
            campaign_id=campaign_id,
            str_id=item['feedback_id']
        )

    return list_unsupported_pagination(
        partial(raw_source.list_feedbacks, campaign_id),
        'feedback',
        id_builder
    )
