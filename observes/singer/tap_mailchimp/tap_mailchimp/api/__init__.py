# Standard libraries
from typing import (
    Any,
    Callable,
    Dict,
    NamedTuple,
    Optional,
)

# Third party libraries
from mailchimp_marketing import (
    Client,
)

# Local libraries
from tap_mailchimp.api import (
    raw as raw_module,
)
from tap_mailchimp.api.raw import (
    RawSource,
)
from tap_mailchimp.common.objs import (
    JSON,
)


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
    conf: Dict[str, str],
    raw_source: RawSource
) -> ApiClient:
    client = Client()
    client.set_config(conf)
    return ApiClient(
        list_audiences=lambda: create_api_data(
            raw_source.list_audiences(client)
        ),
        get_audience=lambda item_id: create_api_data(
            raw_source.get_audience(client, item_id)
        ),
    )


def new_client(conf: Dict[str, str]) -> ApiClient:
    raw_source = raw_module.create_raw_source()
    return new_client_from_source(conf, raw_source)
