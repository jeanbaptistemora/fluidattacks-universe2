from typing import (
    NamedTuple,
)

API_URL = "https://www.zohoapis.com"


class UnexpectedResponse(Exception):
    pass


class PageIndex(NamedTuple):
    page: int
    per_page: int


class DataPageInfo(NamedTuple):
    page: PageIndex
    n_items: int
    more_records: bool
