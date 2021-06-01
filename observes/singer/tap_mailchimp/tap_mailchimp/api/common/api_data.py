import logging
from singer_io import (
    JSON,
)
from typing import (
    Any,
    NamedTuple,
    Optional,
)

LOG = logging.getLogger(__name__)


class ApiData(NamedTuple):
    data: JSON
    links: JSON
    total_items: Optional[int]


def _pop_if_exist(raw: JSON, key: str) -> Any:
    return raw.pop(key) if key in raw else None


def create_api_data(raw: JSON) -> ApiData:
    raw_copy = raw.copy()
    try:
        links = raw_copy.pop("_links")[0]
        total_items = _pop_if_exist(raw_copy, "total_items")
        return ApiData(data=raw_copy, links=links, total_items=total_items)
    except KeyError as error:
        LOG.debug("Bad json: %s", raw_copy)
        raise error
