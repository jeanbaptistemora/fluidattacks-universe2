# Standard libraries
import json

# Third party libraries

# Local libraries
from tap_mailchimp import (
    api,
)
from tap_mailchimp.api import (
    ApiClient,
    AudienceId,
)
from tap_mailchimp.api.common.raw import (
    RawSource,
)
from tap_mailchimp.common.objs import (
    JSON,
)


def _list_audiences() -> JSON:
    with open('./tests/mock_data/audience.json') as data:
        return json.load(data)['list_audiences']


def _get_audience(audience: AudienceId) -> JSON:
    with open('./tests/mock_data/audience.json') as data:
        return json.load(data)['get_audience'][audience.str_id]


def mock_data_source() -> RawSource:
    return RawSource(
        list_audiences=_list_audiences,
        get_audience=_get_audience,
        list_abuse_reports=lambda x: x,  # type: ignore
        get_abuse_report=lambda x: x,  # type: ignore
        get_activity=lambda x: x,  # type: ignore
        get_top_clients=lambda x: x,  # type: ignore
        list_members=lambda x: x,  # type: ignore
        get_member=lambda x: x,  # type: ignore
        list_growth_hist=lambda x: x,  # type: ignore
        get_growth_hist=lambda x: x,  # type: ignore
        list_interest_catg=lambda x: x,  # type: ignore
        get_interest_catg=lambda x: x,  # type: ignore
        get_audience_locations=lambda x: x,  # type: ignore
    )


def new_client() -> ApiClient:
    return api.new_client_from_source(mock_data_source())
