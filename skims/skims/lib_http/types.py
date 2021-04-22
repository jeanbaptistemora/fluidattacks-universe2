# Standard library
from typing import (
    Dict,
    NamedTuple,
)
from urllib.parse import (
    ParseResult,
)

# Third party libraries
import bs4


class URLContext(NamedTuple):
    components: ParseResult
    content: str
    headers_raw: Dict[str, str]
    is_html: bool
    soup: bs4.BeautifulSoup
    url: str

    def __hash__(self) -> int:
        return hash(self.url)

    def __str__(self) -> str:
        return self.url
