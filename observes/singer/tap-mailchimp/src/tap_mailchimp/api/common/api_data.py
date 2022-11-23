# pylint: skip-file
import logging
from returns.maybe import (
    Maybe,
)
from singer_io.singer2.json import (
    JsonObj,
)
from typing import (
    NamedTuple,
    Optional,
)

LOG = logging.getLogger(__name__)


class ApiData(NamedTuple):
    data: JsonObj
    links: JsonObj
    total_items: Optional[int]


def create_api_data(raw: JsonObj) -> ApiData:
    raw_copy = raw.copy()
    try:
        links = raw_copy.pop("_links").to_list()[0].to_json()
        total_items = Maybe.from_optional(
            raw_copy.pop("total_items", None)
        ).map(lambda item: item.to_primitive(int))
        return ApiData(
            data=raw_copy, links=links, total_items=total_items.value_or(None)
        )
    except KeyError as error:
        LOG.debug("Bad json: %s", raw_copy)
        raise error
