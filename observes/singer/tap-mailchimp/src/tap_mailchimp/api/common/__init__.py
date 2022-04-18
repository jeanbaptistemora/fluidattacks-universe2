from itertools import (
    chain,
)
import logging
import math
import paginator
from paginator import (
    PageId,
)
from singer_io.singer2.json import (
    JsonObj,
)
from tap_mailchimp.api.common import (
    api_data,
)
from tap_mailchimp.api.common.api_data import (
    ApiData,
)
from typing import (
    Callable,
    Iterator,
    TypeVar,
)

LOG = logging.getLogger(__name__)
MAX_PER_PAGE = 1000
IdType = TypeVar("IdType")


class NoneTotal(Exception):
    pass


def list_items(
    raw_list: Callable[[PageId], JsonObj],
    items_list_key: str,
    id_builder: Callable[[JsonObj], IdType],
) -> Iterator[IdType]:
    getter: Callable[
        [PageId], ApiData
    ] = lambda page: api_data.create_api_data(raw_list(page))
    test_page = getter(PageId(page=0, per_page=1))
    chunk_size = MAX_PER_PAGE
    if test_page.total_items is None:
        raise NoneTotal()
    total_pages = math.ceil(test_page.total_items / chunk_size)
    pages = paginator.new_page_range(range(total_pages), chunk_size)
    results: Iterator[ApiData] = paginator.get_pages(pages, getter)

    def extract_aud_ids(data: ApiData) -> Iterator[IdType]:
        return iter(
            id_builder(item.to_json())
            for item in data.data[items_list_key].to_list()
        )

    return chain.from_iterable(map(extract_aud_ids, results))


def list_unsupported_pagination(
    raw_list: Callable[[], JsonObj],
    items_list_key: str,
    id_builder: Callable[[JsonObj], IdType],
) -> Iterator[IdType]:
    result = api_data.create_api_data(raw_list())
    if result.total_items is None:
        raise NoneTotal()
    data_list = result.data[items_list_key].to_list()
    if result.total_items > len(data_list):
        LOG.error("Unsupported pagination request miss some items")
    return iter(id_builder(item.to_json()) for item in data_list)
