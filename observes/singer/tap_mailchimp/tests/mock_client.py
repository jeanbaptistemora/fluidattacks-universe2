# Standard libraries
import json

# Third party libraries
from mailchimp_marketing import (
    Client,
)

# Local libraries
from tap_mailchimp.api import (
    ApiClient,
)
from tap_mailchimp import (
    api,
)
from tap_mailchimp.api.raw import (
    RawSource,
)
from tap_mailchimp.common.objs import (
    JSON,
)


def _list_audiences(client: Client) -> JSON:
    # pylint: disable=unused-argument
    with open('./tests/mock_data/audience.json') as data:
        return json.load(data)['list_audiences']


def _get_audience(client: Client, audience_id: str) -> JSON:
    # pylint: disable=unused-argument
    with open('./tests/mock_data/audience.json') as data:
        return json.load(data)['get_audience'][audience_id]


def mock_data_source() -> RawSource:
    return RawSource(
        list_audiences=_list_audiences,
        get_audience=_get_audience
    )


def new_client() -> ApiClient:
    return api.new_client_from_source({}, mock_data_source())
