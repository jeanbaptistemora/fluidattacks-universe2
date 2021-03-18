# Standard libraries
from typing import (
    Iterator,
)

# Third party libraries

# Local libraries
from tap_mailchimp.api.common import (
    api_data,
)
from tap_mailchimp.api.common.api_data import (
    ApiData,
)
from tap_mailchimp.api.common.raw import (
    AbsReportId,
    AudienceId,
    GrowthHistId,
    MemberId,
    RawSource,
)


def get_activity(
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


def get_top_clients(
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


def get_audience(
    raw_source: RawSource,
    audience: AudienceId
) -> ApiData:
    return api_data.create_api_data(
        raw_source.get_audience(audience)
    )


def get_abuse_report(
    raw_source: RawSource,
    report: AbsReportId,
) -> ApiData:
    return api_data.create_api_data(
        raw_source.get_abuse_report(report)
    )


def get_member(
    raw_source: RawSource,
    member: MemberId,
) -> ApiData:
    return api_data.create_api_data(
        raw_source.get_member(member)
    )


def get_growth_hist(
    raw_source: RawSource,
    ghist: GrowthHistId,
) -> ApiData:
    return api_data.create_api_data(
        raw_source.get_growth_hist(ghist)
    )
