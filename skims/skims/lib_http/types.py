import aiohttp
import bs4
from typing import (
    Dict,
    NamedTuple,
    Optional,
)
from urllib.parse import (
    ParseResult,
    urlsplit,
)


class URLContext(NamedTuple):
    components: ParseResult
    content: str
    custom_f023: Optional[aiohttp.ClientResponse]
    has_redirect: bool
    headers_raw: Dict[str, str]
    is_html: bool
    original_url: str
    soup: bs4.BeautifulSoup
    timestamp_ntp: Optional[float]
    url: str
    response_status: int

    def __hash__(self) -> int:
        return hash(self.url)

    def __str__(self) -> str:
        return self.url

    def get_base_domain(self) -> str:
        base_domain = urlsplit(self.url).netloc
        if base_domain.startswith("www."):
            base_domain = base_domain.replace("www.", "", 1)
        if base_domain.startswith("www3."):
            base_domain = base_domain.replace("www3.", "", 1)
        return base_domain
