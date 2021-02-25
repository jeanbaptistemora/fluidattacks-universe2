# Standard libraries
# Third party libraries
from mailchimp_marketing import (
    Client,
)
# Local libraries
from tap_mailchimp.common import JSON


def list_audiences(client: Client) -> JSON:
    return client.lists.get_all_lists(fields='id')


def get_audience(client: Client, audience_id: str) -> JSON:
    return client.lists.get_list(audience_id)


def list_abuse_reports(client: Client, audience_id: str) -> JSON:
    return client.lists.get_list_abuse_reports(audience_id)


def get_abuse_report(
    client: Client,
    audience_id: str,
    report_id: str
) -> JSON:
    return client.lists.get_list_abuse_report_details(
        audience_id, report_id
    )


def get_activity(client: Client, audience_id: str) -> JSON:
    return client.lists.get_list_recent_activity(audience_id)


def get_clients(client: Client, audience_id: str) -> JSON:
    return client.lists.get_list_clients(audience_id)


def get_members(client: Client, audience_id: str) -> JSON:
    return client.lists.get_list_members_info(audience_id)
