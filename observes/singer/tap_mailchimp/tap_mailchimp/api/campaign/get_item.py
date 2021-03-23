# Standard libraries

# Third party libraries

# Local libraries
from tap_mailchimp.api.common import (
    api_data,
)
from tap_mailchimp.api.common.api_data import (
    ApiData,
)
from tap_mailchimp.api.common.raw import (
    CampaignId,
    RawSource,
)


def get_campaign(
    raw_source: RawSource,
    campaign: CampaignId,
) -> ApiData:
    return api_data.create_api_data(
        raw_source.get_campaign(campaign)
    )
