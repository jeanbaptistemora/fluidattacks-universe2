# Standard libraries
from typing import (
    Callable,
    NamedTuple,
    Union,
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


class AudienceId(NamedTuple):
    str_id: str


class AbsReportId(NamedTuple):
    audience_id: AudienceId
    str_id: str


ItemId = Union[AudienceId, AbsReportId]


class RawSource(NamedTuple):
    list_audiences: Callable[[Client], JSON]
    get_audience: Callable[[Client, AudienceId], JSON]
    list_abuse_reports: Callable[[Client, AudienceId], JSON]
    get_abuse_report: Callable[[Client, AbsReportId], JSON]
    get_activity: Callable[[Client, AudienceId], JSON]


def _list_audiences(client: Client) -> JSON:
    result = client.lists.get_all_lists(
        fields=['lists.id', 'total_items', '_links']
    )
    LOG.debug('_list_audiences response: %s', result)
    return result


def _get_audience(client: Client, audience: AudienceId) -> JSON:
    return client.lists.get_list(audience.str_id)


def _list_abuse_reports(client: Client, audience: AudienceId) -> JSON:
    result = client.lists.get_list_abuse_reports(
        audience.str_id,
        fields=['abuse_reports.id', 'total_items', '_links']
    )
    LOG.debug('_list_abuse_reports response: %s', result)
    return result


def _get_abuse_report(client: Client, report: AbsReportId) -> JSON:
    return client.lists.get_list_abuse_report_details(
        report.audience_id.str_id, report.str_id
    )


def _get_activity(client: Client, audience_id: AudienceId) -> JSON:
    return client.lists.get_list_recent_activity(audience_id.str_id)


def _get_clients(client: Client, audience_id: str) -> JSON:
    return client.lists.get_list_clients(audience_id)


def _get_members(client: Client, audience_id: str) -> JSON:
    return client.lists.get_list_members_info(audience_id)


def create_raw_source() -> RawSource:
    return RawSource(
        list_audiences=_list_audiences,
        get_audience=_get_audience,
        list_abuse_reports=_list_abuse_reports,
        get_abuse_report=_get_abuse_report,
        get_activity=_get_activity,
    )
