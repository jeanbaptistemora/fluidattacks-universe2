# Standard libraries
from functools import partial
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
import utils_logger
from tap_mailchimp.common.objs import (
    JSON,
)


LOG = utils_logger.get_log(__name__)


class AudienceId(NamedTuple):
    str_id: str


class AbsReportId(NamedTuple):
    audience_id: AudienceId
    str_id: str


class GrowthHistId(NamedTuple):
    audience_id: AudienceId
    str_id: str


class InterestCatgId(NamedTuple):
    audience_id: AudienceId
    str_id: str


class MemberId(NamedTuple):
    audience_id: AudienceId
    str_id: str


ItemId = Union[
    AudienceId,
    AbsReportId,
    GrowthHistId,
    InterestCatgId,
    MemberId,
]


class RawSource(NamedTuple):
    list_audiences: Callable[[], JSON]
    get_audience: Callable[[AudienceId], JSON]
    list_abuse_reports: Callable[[AudienceId], JSON]
    get_abuse_report: Callable[[AbsReportId], JSON]
    get_activity: Callable[[AudienceId], JSON]
    get_top_clients: Callable[[AudienceId], JSON]
    list_members: Callable[[AudienceId], JSON]
    get_member: Callable[[MemberId], JSON]
    list_growth_hist: Callable[[AudienceId], JSON]
    get_growth_hist: Callable[[GrowthHistId], JSON]
    list_interest_catg: Callable[[AudienceId], JSON]
    get_interest_catg: Callable[[InterestCatgId], JSON]


def _list_audiences(client: Client) -> JSON:
    result = client.lists.get_all_lists(
        fields=['lists.id', 'total_items', '_links']
    )
    LOG.debug('_list_audiences response: %s', result)
    return result


def _get_audience(client: Client, audience_id: AudienceId) -> JSON:
    return client.lists.get_list(audience_id.str_id)


def _list_abuse_reports(client: Client, audience_id: AudienceId) -> JSON:
    result = client.lists.get_list_abuse_reports(
        audience_id.str_id,
        fields=['abuse_reports.id', 'total_items', '_links']
    )
    LOG.debug('_list_abuse_reports response: %s', result)
    return result


def _get_abuse_report(client: Client, report_id: AbsReportId) -> JSON:
    return client.lists.get_list_abuse_report_details(
        report_id.audience_id.str_id, report_id.str_id
    )


def _get_activity(client: Client, audience_id: AudienceId) -> JSON:
    return client.lists.get_list_recent_activity(audience_id.str_id)


def _get_clients(client: Client, audience_id: AudienceId) -> JSON:
    return client.lists.get_list_clients(audience_id.str_id)


def _list_members(client: Client, audience_id: AudienceId) -> JSON:
    return client.lists.get_list_members_info(
        audience_id.str_id,
        fields=['members.id', 'total_items', '_links']
    )


def _get_member(client: Client, member_id: MemberId) -> JSON:
    return client.lists.get_list_member(
        member_id.audience_id.str_id,
        member_id.str_id,
        exclude_fields=['tags']
    )


def _list_growth_hist(client: Client, audience_id: AudienceId) -> JSON:
    return client.lists.get_list_growth_history(
        audience_id.str_id,
        fields=['history.month', 'total_items', '_links']
    )


def _get_growth_hist(client: Client, ghist_id: GrowthHistId) -> JSON:
    return client.lists.get_list_growth_history_by_month(
        ghist_id.audience_id.str_id,
        ghist_id.str_id
    )


def _list_interest_catg(client: Client, audience_id: AudienceId) -> JSON:
    return client.lists.get_list_interest_categories(
        audience_id.str_id,
        fields=['categories.id', 'total_items', '_links']
    )


def _get_interest_catg(client: Client, interest_id: InterestCatgId) -> JSON:
    return client.lists.get_interest_category(
        interest_id.audience_id.str_id,
        interest_id.str_id
    )


def create_raw_source(client: Client) -> RawSource:
    return RawSource(
        list_audiences=partial(_list_audiences, client),
        get_audience=partial(_get_audience, client),
        list_abuse_reports=partial(_list_abuse_reports, client),
        get_abuse_report=partial(_get_abuse_report, client),
        get_activity=partial(_get_activity, client),
        get_top_clients=partial(_get_clients, client),
        list_members=partial(_list_members, client),
        get_member=partial(_get_member, client),
        list_growth_hist=partial(_list_growth_hist, client),
        get_growth_hist=partial(_get_growth_hist, client),
        list_interest_catg=partial(_list_interest_catg, client),
        get_interest_catg=partial(_get_interest_catg, client),
    )
