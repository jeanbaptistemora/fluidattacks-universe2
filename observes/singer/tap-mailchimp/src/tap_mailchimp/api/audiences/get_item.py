from singer_io.singer2.json import (
    JsonValue,
)
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
    InterestCatgId,
    MemberId,
    RawSource,
)
from typing import (
    Iterator,
)


def get_activity(
    raw_source: RawSource, audience: AudienceId
) -> Iterator[ApiData]:
    result = api_data.create_api_data(raw_source.get_activity(audience))
    activity = [
        item.to_json().copy() for item in result.data["activity"].to_list()
    ]
    audience_id = result.data["list_id"]
    for data in activity:
        data["list_id"] = audience_id
        if "_links" not in data:
            data["_links"] = JsonValue([JsonValue({})])
    return iter(map(api_data.create_api_data, activity))


def get_top_clients(
    raw_source: RawSource, audience: AudienceId
) -> Iterator[ApiData]:
    result = api_data.create_api_data(raw_source.get_top_clients(audience))
    clients = [
        item.to_json().copy() for item in result.data["clients"].to_list()
    ]
    audience_id = result.data["list_id"]
    for data in clients:
        data["list_id"] = audience_id
        data["_links"] = JsonValue([JsonValue({})])
    return iter(map(api_data.create_api_data, clients))


def get_audience(raw_source: RawSource, audience: AudienceId) -> ApiData:
    return api_data.create_api_data(raw_source.get_audience(audience))


def get_abuse_report(
    raw_source: RawSource,
    report: AbsReportId,
) -> ApiData:
    return api_data.create_api_data(raw_source.get_abuse_report(report))


def get_member(
    raw_source: RawSource,
    member: MemberId,
) -> ApiData:
    return api_data.create_api_data(raw_source.get_member(member))


def get_growth_hist(
    raw_source: RawSource,
    ghist: GrowthHistId,
) -> ApiData:
    return api_data.create_api_data(raw_source.get_growth_hist(ghist))


def get_interest_catg(
    raw_source: RawSource,
    interest_catg: InterestCatgId,
) -> ApiData:
    return api_data.create_api_data(
        raw_source.get_interest_catg(interest_catg)
    )


def get_audience_locations(
    raw_source: RawSource,
    audience: AudienceId,
) -> Iterator[ApiData]:
    result = api_data.create_api_data(
        raw_source.get_audience_locations(audience)
    )
    locations = [
        item.to_json().copy() for item in result.data["locations"].to_list()
    ]
    audience_id = result.data["list_id"]
    for data in locations:
        data["list_id"] = audience_id
        data["_links"] = JsonValue([JsonValue({})])
    return iter(map(api_data.create_api_data, locations))
