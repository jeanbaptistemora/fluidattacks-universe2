from dynamodb.types import (
    PageInfo,
)
from typing import (
    Any,
    NamedTuple,
)

Item = dict[str, Any]


class SearchResponse(NamedTuple):
    items: tuple[Item, ...]
    page_info: PageInfo
    total: int
