# Standard libraries
import math
import logging
from itertools import (
    chain,
)
from typing import (
    Callable,
    Dict,
    Iterator,
    TypeVar,
)

# Third party libraries

# Local libraries
import paginator
from paginator import (
    PageId,
)
from tap_mailchimp.api.common import (
    api_data,
)
from tap_mailchimp.api.common.api_data import (
    ApiData,
)
from tap_mailchimp.common.objs import (
    JSON,
)


LOG = logging.getLogger(__name__)
MAX_PER_PAGE = 1000
SomeId = TypeVar('SomeId')


class NoneTotal(Exception):
    pass


def list_items(
    raw_list: Callable[[PageId], JSON],
    items_list_key: str,
    id_builder: Callable[[Dict[str, str]], SomeId]
) -> Iterator[SomeId]:
    getter: Callable[[PageId], ApiData] = (
        lambda page: api_data.create_api_data(
            raw_list(page)
        )
    )
    test_page = getter(PageId(page=0, per_page=1))
    chunk_size = MAX_PER_PAGE
    if test_page.total_items is None:
        raise NoneTotal()
    total_pages = math.ceil(test_page.total_items / chunk_size)
    pages = paginator.new_page_range(range(total_pages), chunk_size)
    results: Iterator[ApiData] = paginator.get_pages(pages, getter)

    def extract_aud_ids(a_data: ApiData) -> Iterator[SomeId]:
        audiences_data = a_data.data[items_list_key]
        return iter(map(id_builder, audiences_data))

    return chain.from_iterable(map(extract_aud_ids, results))
