# Standard libraries
from typing import (
    Any,
    Callable,
    NamedTuple,
    Optional,
)

# Third party libraries
from mailchimp_marketing import (
    Client,
)

# Local libraries
from tap_mailchimp import (
    auth,
    common,
)
from tap_mailchimp.api import (
    raw as raw_module,
)


Credentials = auth.Credentials
JSON = common.objs.JSON
RawSource = raw_module.RawSource


class ApiData(NamedTuple):
    data: JSON
    links: JSON
    total_items: Optional[int]


class ApiClient(NamedTuple):
    list_audiences: Callable[[], ApiData]
    get_audience: Callable[[str], ApiData]


def _pop_if_exist(raw: JSON, key: str) -> Any:
    return raw.pop(key) if key in raw else None


def create_api_data(raw: JSON) -> ApiData:
    links = raw.pop('_links')[0]
    total_items = _pop_if_exist(raw, 'total_items')
    return ApiData(
        data=raw,
        links=links,
        total_items=total_items
    )


def new_client_from_source(
    creds: Credentials,
    raw_source: RawSource
) -> ApiClient:
    client = Client()
    client.set_config({
        'api_key': creds.api_key,
        'server': creds.dc
    })
    return ApiClient(
        list_audiences=lambda: create_api_data(
            raw_source.list_audiences(client)
        ),
        get_audience=lambda item_id: create_api_data(
            raw_source.get_audience(client, item_id)
        ),
    )


def new_client(creds: Credentials) -> ApiClient:
    raw_source = raw_module.create_raw_source()
    return new_client_from_source(creds, raw_source)
