# Standard libraries
from functools import partial
from typing import (
    Any,
    Callable,
    Dict,
    NamedTuple,
    Optional
)
# Third party libraries
from mailchimp_marketing import (
    Client,
)
# Local libraries


JSON = Dict[str, Any]


class ApiData(NamedTuple):
    data: JSON
    links: JSON
    total_items: Optional[int]


class ApiClient(NamedTuple):
    list_audiences: Callable[[], ApiData]
    get_audience: Callable[[str], ApiData]
    list_abuse_reports: Callable[[str], ApiData]
    get_abuse_report: Callable[[str, str], ApiData]
    get_activity: Callable[[str], ApiData]
    get_clients: Callable[[str], ApiData]
    get_members: Callable[[str], ApiData]


def _list_audiences(client: Client) -> ApiData:
    raw = client.lists.get_all_lists()
    return ApiData(
        data=raw['lists'],
        links=raw['_links'],
        total_items=raw['total_items']
    )


def _get_audience(client: Client, audience_id: str) -> ApiData:
    raw = client.lists.get_list(audience_id)
    links = raw.pop('_links')
    return ApiData(
        data=raw,
        links=links,
        total_items=None
    )


def _list_abuse_reports(client: Client, audience_id: str) -> ApiData:
    raw = client.lists.get_list_abuse_reports(audience_id)
    return ApiData(
        data=raw['abuse_reports'],
        links=raw['_links'],
        total_items=raw['total_items']
    )


def _get_abuse_report(
    client: Client,
    audience_id: str,
    report_id: str
) -> ApiData:
    raw = client.lists.get_list_abuse_report_details(
        audience_id, report_id
    )
    links = raw.pop('_links')
    return ApiData(
        data=raw,
        links=links,
        total_items=None
    )


def _get_activity(client: Client, audience_id: str) -> ApiData:
    raw = client.lists.get_list_recent_activity(audience_id)
    return ApiData(
        data=raw['activity'],
        links=raw['_links'],
        total_items=None
    )


def _get_clients(client: Client, audience_id: str) -> ApiData:
    raw = client.lists.get_list_clients(audience_id)
    return ApiData(
        data=raw['clients'],
        links=raw['_links'],
        total_items=None
    )


def _get_members(client: Client, audience_id: str) -> ApiData:
    raw = client.lists.get_list_members_info(audience_id)
    return ApiData(
        data=raw['members'],
        links=raw['_links'],
        total_items=raw['total_items']
    )


def new_client() -> ApiClient:
    client = Client()
    client.set_config({
        "api_key": "YOUR_API_KEY",
        "server": "YOUR_SERVER_PREFIX"
    })
    return ApiClient(
        list_audiences=partial(_list_audiences, client),
        get_audience=partial(_get_audience, client),
        list_abuse_reports=partial(_list_abuse_reports, client),
        get_abuse_report=partial(_get_abuse_report, client),
        get_activity=partial(_get_activity, client),
        get_clients=partial(_get_clients, client),
        get_members=partial(_get_members, client)
    )
