# Standard libraries
from functools import partial
from typing import (
    Any,
    Callable,
    Iterator,
    NamedTuple,
    Optional,
)

# Third party libraries
from mailchimp_marketing import (
    Client,
)

# Local libraries
from tap_mailchimp import (
    utils
)
from tap_mailchimp.api import (
    raw as raw_module,
)
from tap_mailchimp.auth import (
    Credentials,
)
from tap_mailchimp.common.objs import (
    JSON,
)

AbsReportId = raw_module.AbsReportId
AudienceId = raw_module.AudienceId
ItemId = raw_module.ItemId
RawSource = raw_module.RawSource
LOG = utils.get_log(__name__)


class ApiData(NamedTuple):
    data: JSON
    links: JSON
    total_items: Optional[int]


class ApiClient(NamedTuple):
    list_audiences: Callable[[], Iterator[AudienceId]]
    get_audience: Callable[[AudienceId], ApiData]
    list_abuse_reports: Callable[[AudienceId], Iterator[AbsReportId]]
    get_abuse_report: Callable[[AbsReportId], ApiData]
    get_activity: Callable[[AudienceId], Iterator[ApiData]]
    get_top_clients: Callable[[AudienceId], Iterator[ApiData]]


def _pop_if_exist(raw: JSON, key: str) -> Any:
    return raw.pop(key) if key in raw else None


def create_api_data(raw: JSON) -> ApiData:
    try:
        links = raw.pop('_links')[0]
        total_items = _pop_if_exist(raw, 'total_items')
        return ApiData(
            data=raw,
            links=links,
            total_items=total_items
        )
    except KeyError as error:
        LOG.debug('Bad json: %s', raw)
        raise error


def _get_activity(
    raw_source: RawSource,
    client: Client,
    audience: AudienceId
) -> Iterator[ApiData]:
    result = create_api_data(
        raw_source.get_activity(client, audience)
    )
    audience_id = result.data['list_id']
    for data in result.data['activity']:
        data['list_id'] = audience_id
        if '_links' not in data:
            data['_links'] = [{}]
    return iter(map(
        create_api_data,
        result.data['activity']
    ))


def _get_top_clients(
    raw_source: RawSource,
    client: Client,
    audience: AudienceId
) -> Iterator[ApiData]:
    result = create_api_data(
        raw_source.get_top_clients(client, audience)
    )
    audience_id = result.data['list_id']
    for data in result.data['clients']:
        data['list_id'] = audience_id
        data['_links'] = [{}]
    return iter(map(
        create_api_data,
        result.data['clients']
    ))


def _list_audiences(
    raw_source: RawSource,
    client: Client,
) -> Iterator[AudienceId]:
    result = create_api_data(
        raw_source.list_audiences(client)
    )
    audiences_data = result.data['lists']
    return iter(map(lambda a: AudienceId(a['id']), audiences_data))


def _list_abuse_reports(
    raw_source: RawSource,
    client: Client,
    audience: AudienceId
) -> Iterator[AbsReportId]:
    result = create_api_data(
        raw_source.list_abuse_reports(client, audience)
    )
    data = result.data['abuse_reports']
    return iter(map(
        lambda item: AbsReportId(
            audience_id=audience,
            str_id=item['id']
        ),
        data
    ))


def new_client_from_source(
    creds: Credentials,
    raw_source: RawSource
) -> ApiClient:
    client = Client()
    client.set_config({
        'api_key': creds.api_key,
        'server': creds.dc
    })
    return ApiClient(
        list_audiences=partial(_list_audiences, raw_source, client),
        get_audience=lambda item_id: create_api_data(
            raw_source.get_audience(client, item_id)
        ),
        list_abuse_reports=partial(_list_abuse_reports, raw_source, client),
        get_abuse_report=lambda item_id: create_api_data(
            raw_source.get_abuse_report(client, item_id)
        ),
        get_activity=partial(_get_activity, raw_source, client),
        get_top_clients=partial(_get_top_clients, raw_source, client),
    )


def new_client(creds: Credentials) -> ApiClient:
    raw_source = raw_module.create_raw_source()
    return new_client_from_source(creds, raw_source)
