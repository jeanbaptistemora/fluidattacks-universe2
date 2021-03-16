# Standard libraries
from functools import partial
from typing import (
    Any,
    Callable,
    NamedTuple,
    Optional,
)

# Third party libraries
from mailchimp_marketing import (
    Client,
)

# Local libraries
from tap_mailchimp.common.objs import (
    JSON,
)
from tap_mailchimp.api import (
    raw as raw_module,
)
from tap_mailchimp.auth import (
    Credentials,
)


AbsReportId = raw_module.AbsReportId
AudienceId = raw_module.AudienceId
ItemId = raw_module.ItemId
RawSource = raw_module.RawSource


class ApiData(NamedTuple):
    data: JSON
    links: JSON
    total_items: Optional[int]


class ApiClient(NamedTuple):
    list_audiences: Callable[[], ApiData]
    get_audience: Callable[[AudienceId], ApiData]
    list_abuse_reports: Callable[[AudienceId], ApiData]
    get_abuse_report: Callable[[AbsReportId], ApiData]
    get_activity: Callable[[AudienceId], ApiData]
    get_top_clients: Callable[[AudienceId], ApiData]


def _pop_if_exist(raw: JSON, key: str) -> Any:
    return raw.pop(key) if key in raw else None


def create_api_data(raw: JSON) -> ApiData:
    links = raw.pop('_links')[0]
    total_items = _pop_if_exist(raw, 'total_items')
    return ApiData(
        data=raw,
        links=links,
        total_items=total_items
    )


def _get_activity(
    raw_source: RawSource,
    client: Client,
    audience: AudienceId
) -> ApiData:
    result = create_api_data(
        raw_source.get_activity(client, audience)
    )
    list_id = result.data['list_id']
    for data in result.data['activity']:
        data['list_id'] = list_id
    return result


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
        list_audiences=lambda: create_api_data(
            raw_source.list_audiences(client)
        ),
        get_audience=lambda item_id: create_api_data(
            raw_source.get_audience(client, item_id)
        ),
        list_abuse_reports=lambda item_id: create_api_data(
            raw_source.list_abuse_reports(client, item_id)
        ),
        get_abuse_report=lambda item_id: create_api_data(
            raw_source.get_abuse_report(client, item_id)
        ),
        get_activity=partial(_get_activity, raw_source, client),
        get_top_clients=lambda item_id: create_api_data(
            raw_source.get_top_clients(client, item_id)
        ),
    )


def new_client(creds: Credentials) -> ApiClient:
    raw_source = raw_module.create_raw_source()
    return new_client_from_source(creds, raw_source)
