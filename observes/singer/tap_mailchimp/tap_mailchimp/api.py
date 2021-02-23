# Standard libraries
from typing import (
    Any,
    Dict,
    NamedTuple,
    Optional
)
# Third party libraries
from mailchimp_marketing import Client as ApiClient
# Local libraries


JSON = Dict[str, Any]


class ApiData(NamedTuple):
    data: JSON
    links: JSON
    total_items: Optional[int]


def list_audiences(client: ApiClient) -> ApiData:
    raw = client.lists.get_all_lists()
    return ApiData(
        data=raw['lists'],
        links=raw['_links'],
        total_items=raw['total_items']
    )


def get_audience(client: ApiClient, audience_id: str) -> ApiData:
    raw = client.lists.get_list(audience_id)
    links = raw.pop('_links')
    return ApiData(
        data=raw,
        links=links,
        total_items=None
    )


def list_abuse_reports(client: ApiClient, audience_id: str) -> ApiData:
    raw = client.lists.get_list_abuse_reports(audience_id)
    return ApiData(
        data=raw['abuse_reports'],
        links=raw['_links'],
        total_items=raw['total_items']
    )


def get_abuse_report(
    client: ApiClient,
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


def get_activity(client: ApiClient, audience_id: str) -> ApiData:
    raw = client.lists.get_list_recent_activity(audience_id)
    return ApiData(
        data=raw['activity'],
        links=raw['_links'],
        total_items=None
    )


def get_clients(client: ApiClient, audience_id: str) -> ApiData:
    raw = client.lists.get_list_clients(audience_id)
    return ApiData(
        data=raw['clients'],
        links=raw['_links'],
        total_items=None
    )


def get_members(client: ApiClient, audience_id: str) -> ApiData:
    raw = client.lists.get_list_members_info(audience_id)
    return ApiData(
        data=raw['members'],
        links=raw['_links'],
        total_items=raw['total_items']
    )
