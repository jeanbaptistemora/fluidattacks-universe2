# Standard libraries
from typing import (
    Iterator,
)

# Third party libraries

# Local libraries
import utils_logger
from tap_mailchimp.api.common import (
    api_data,
    list_items_alert,
)
from tap_mailchimp.api.common.raw import (
    CampaignId,
    RawSource,
)

LOG = utils_logger.get_log(__name__)


def list_campaigns(
    raw_source: RawSource,
) -> Iterator[CampaignId]:
    result = api_data.create_api_data(
        raw_source.list_campaigns()
    )
    list_items_alert(
        'list_campaigns',
        result.total_items
    )
    LOG.debug('list_campaigns result: %s', result)
    data = result.data['campaigns']
    return iter(map(
        lambda item: CampaignId(
            str_id=item['id']
        ),
        data
    ))
