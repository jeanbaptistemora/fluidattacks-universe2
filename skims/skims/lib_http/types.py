# Standard library
from typing import (
    Dict,
    NamedTuple,
    Optional,
)
from urllib.parse import (
    ParseResult,
)
import aiohttp

# Third party libraries
import bs4


class URLContext(NamedTuple):
    components: ParseResult
    content: str
    custom_f023: Optional[aiohttp.ClientResponse]
    headers_raw: Dict[str, str]
    is_html: bool
    soup: bs4.BeautifulSoup
    timestamp_ntp: Optional[float]
    url: str

    def __hash__(self) -> int:
        return hash(self.url)

    def __str__(self) -> str:
        return self.url
