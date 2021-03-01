# Standard libraries
import json
from typing import (
    Union,
)
# Third party libraries
from mailchimp_marketing import (
    Client,
)

# Local libraries
from tap_mailchimp import (
    api,
    auth,
    common
)


ApiClient = Union[api.ApiClient]
Credentials = Union[auth.Credentials]
JSON = Union[common.objs.JSON]
RawSource = Union[api.raw.RawSource]


def _list_audiences(client: Client) -> JSON:
    # pylint: disable=unused-argument
    with open('./tests/mock_data/audience.json') as data:
        return json.load(data)['list_audiences']


def _get_audience(client: Client, audience_id: str) -> JSON:
    # pylint: disable=unused-argument
    with open('./tests/mock_data/audience.json') as data:
        return json.load(data)['get_audience'][audience_id]


def mock_creds() -> Credentials:
    return auth.to_credentials({
        'api_key': 'the_key',
        'dc': 'the_prefix',
    })


def mock_data_source() -> RawSource:
    return RawSource(
        list_audiences=_list_audiences,
        get_audience=_get_audience
    )


def new_client() -> ApiClient:
    return api.new_client_from_source(mock_creds(), mock_data_source())
