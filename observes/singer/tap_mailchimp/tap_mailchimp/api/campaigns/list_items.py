# Standard libraries
import logging
from typing import (
    Dict,
    Iterator,
)

# Third party libraries

# Local libraries
from tap_mailchimp.api.common import (
    list_items,
)
from tap_mailchimp.api.common.raw import (
    CampaignId,
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
