# Standard libraries
from typing import (
    Callable,
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
from tap_mailchimp.common.objs import (
    JSON,
)


LOG = utils.get_log(__name__)


class RawSource(NamedTuple):
    list_audiences: Callable[[Client], JSON]
    get_audience: Callable[[Client, str], JSON]


def _list_audiences(client: Client) -> JSON:
    result = client.lists.get_all_lists(
        fields=['lists.id', 'total_items', '_links']
    )
    LOG.debug('_list_audiences response: %s', result)
    return result


def _get_audience(client: Client, audience_id: str) -> JSON:
    return client.lists.get_list(audience_id)


def _list_abuse_reports(client: Client, audience_id: str) -> JSON:
    return client.lists.get_list_abuse_reports(audience_id)


def _get_abuse_report(
    client: Client,
    audience_id: str,
    report_id: str
) -> JSON:
    return client.lists.get_list_abuse_report_details(
        audience_id, report_id
    )


def _get_activity(client: Client, audience_id: str) -> JSON:
    return client.lists.get_list_recent_activity(audience_id)


def _get_clients(client: Client, audience_id: str) -> JSON:
    return client.lists.get_list_clients(audience_id)


def _get_members(client: Client, audience_id: str) -> JSON:
    return client.lists.get_list_members_info(audience_id)


def create_raw_source() -> RawSource:
    return RawSource(
        list_audiences=_list_audiences,
        get_audience=_get_audience
    )
