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
        list_abuse_reports=lambda x: x,
        get_abuse_report=lambda x: x,
        get_activity=lambda x: x,
        get_top_clients=lambda x: x,
        list_members=lambda x: x,
        get_member=lambda x: x,
        list_growth_hist=lambda x: x,
        get_growth_hist=lambda x: x,
        list_interest_catg=lambda x: x,
        get_interest_catg=lambda x: x,
    )


def new_client() -> ApiClient:
    return api.new_client_from_source(mock_data_source())
