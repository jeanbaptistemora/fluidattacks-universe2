# Standard libraries
from functools import partial
from typing import (
    Callable,
    Iterator,
    NamedTuple,
)

# Third party libraries
from mailchimp_marketing import (
    Client,
)

# Local libraries
import utils_logger
from tap_mailchimp.api.audiences import (
    get_item,
    list_items,
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
    GrowthHistId,
    ItemId,
    InterestCatgId,
    MemberId,
    RawSource,
)
from tap_mailchimp.auth import (
    Credentials,
)

LOG = utils_logger.get_log(__name__)


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


def new_client_from_source(
    raw_source: RawSource
) -> ApiClient:
    return ApiClient(
        list_audiences=partial(list_items.list_audiences, raw_source),
        get_audience=partial(get_item.get_audience, raw_source),
        list_abuse_reports=partial(list_items.list_abuse_reports, raw_source),
        get_abuse_report=partial(get_item.get_abuse_report, raw_source),
        get_activity=partial(get_item.get_activity, raw_source),
        get_top_clients=partial(get_item.get_top_clients, raw_source),
        list_members=partial(list_items.list_members, raw_source),
        get_member=partial(get_item.get_member, raw_source),
        list_growth_hist=partial(list_items.list_growth_hist, raw_source),
        get_growth_hist=partial(get_item.get_growth_hist, raw_source),
        list_interest_catg=partial(list_items.list_interest_catg, raw_source),
        get_interest_catg=partial(get_item.get_interest_catg, raw_source),
        get_audience_locations=partial(
            get_item.get_audience_locations, raw_source
        ),
    )


def new_client(creds: Credentials) -> ApiClient:
    client = Client()
    client.set_config({
        'api_key': creds.api_key,
        'server': creds.dc
    })
    raw_source = raw_module.create_raw_source(client)
    return new_client_from_source(raw_source)


# export types
__all__ = [
    'AbsReportId',
    'ApiData',
    'AudienceId',
    'GrowthHistId',
    'ItemId',
    'InterestCatgId',
    'MemberId',
    'RawSource',
]
