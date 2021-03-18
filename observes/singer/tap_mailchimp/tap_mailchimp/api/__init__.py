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
from tap_mailchimp import (
    utils
)
from tap_mailchimp.api.common import (
    api_data,
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
    MemberId,
    RawSource,
)
from tap_mailchimp.auth import (
    Credentials,
)

LOG = utils.get_log(__name__)


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


def _get_activity(
    raw_source: RawSource,
    audience: AudienceId
) -> Iterator[ApiData]:
    result = api_data.create_api_data(
        raw_source.get_activity(audience)
    )
    activity = result.data['activity'].copy()
    audience_id = result.data['list_id']
    for data in activity:
        data['list_id'] = audience_id
        if '_links' not in data:
            data['_links'] = [{}]
    return iter(map(
        api_data.create_api_data,
        activity
    ))


def _get_top_clients(
    raw_source: RawSource,
    audience: AudienceId
) -> Iterator[ApiData]:
    result = api_data.create_api_data(
        raw_source.get_top_clients(audience)
    )
    clients = result.data['clients'].copy()
    audience_id = result.data['list_id']
    for data in clients:
        data['list_id'] = audience_id
        data['_links'] = [{}]
    return iter(map(
        api_data.create_api_data,
        clients
    ))


def _list_audiences(
    raw_source: RawSource,
) -> Iterator[AudienceId]:
    result = api_data.create_api_data(
        raw_source.list_audiences()
    )
    audiences_data = result.data['lists']
    return iter(map(lambda a: AudienceId(a['id']), audiences_data))


def _list_abuse_reports(
    raw_source: RawSource,
    audience: AudienceId
) -> Iterator[AbsReportId]:
    result = api_data.create_api_data(
        raw_source.list_abuse_reports(audience)
    )
    data = result.data['abuse_reports']
    return iter(map(
        lambda item: AbsReportId(
            audience_id=audience,
            str_id=item['id']
        ),
        data
    ))


def _list_members(
    raw_source: RawSource,
    audience: AudienceId
) -> Iterator[MemberId]:
    result = api_data.create_api_data(
        raw_source.list_members(audience)
    )
    data = result.data['members']
    return iter(map(
        lambda item: MemberId(
            audience_id=audience,
            str_id=item['id']
        ),
        data
    ))


def _list_growth_hist(
    raw_source: RawSource,
    audience: AudienceId
) -> Iterator[GrowthHistId]:
    result = api_data.create_api_data(
        raw_source.list_growth_hist(audience)
    )
    data = result.data['history']
    return iter(map(
        lambda item: GrowthHistId(
            audience_id=audience,
            str_id=item['month']
        ),
        data
    ))


def new_client_from_source(
    raw_source: RawSource
) -> ApiClient:
    return ApiClient(
        list_audiences=partial(_list_audiences, raw_source),
        get_audience=lambda item_id: api_data.create_api_data(
            raw_source.get_audience(item_id)
        ),
        list_abuse_reports=partial(_list_abuse_reports, raw_source),
        get_abuse_report=lambda item_id: api_data.create_api_data(
            raw_source.get_abuse_report(item_id)
        ),
        get_activity=partial(_get_activity, raw_source),
        get_top_clients=partial(_get_top_clients, raw_source),
        list_members=partial(_list_members, raw_source),
        get_member=lambda item_id: api_data.create_api_data(
            raw_source.get_member(item_id)
        ),
        list_growth_hist=partial(_list_growth_hist, raw_source),
        get_growth_hist=lambda item_id: api_data.create_api_data(
            raw_source.get_growth_hist(item_id)
        )
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
    'MemberId',
    'RawSource',
]
