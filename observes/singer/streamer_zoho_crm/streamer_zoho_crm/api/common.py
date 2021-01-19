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


class DataPageInfo(NamedTuple):
    page: int
    n_items: int
    per_page: int
    more_records: bool
