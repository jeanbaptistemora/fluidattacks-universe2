# Standard libraries
from typing import (
    Any,
    Dict,
    NamedTuple,
)
# Third party libraries
# Local libraries


JSON = Dict[str, Any]
API_URL = 'https://www.zohoapis.com'


class UnexpectedResponse(Exception):
    pass


class PageIndex(NamedTuple):
    page: int
    per_page: int


class DataPageInfo(NamedTuple):
    page: PageIndex
    n_items: int
    more_records: bool
