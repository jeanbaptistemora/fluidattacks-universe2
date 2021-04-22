# Standard library
from string import (
    whitespace,
)
from typing import (
    Iterable,
    Optional,
)
from urllib.parse import (
    urlparse,
    ParseResult,
)

# Third party libraries
from bs4 import (
    BeautifulSoup,
)


def is_html(string: str, soup: Optional[BeautifulSoup] = None) -> bool:
    string = string.strip(whitespace)

    if string.startswith('{'):
        # JSON
        return False

    if soup is None:
        soup = BeautifulSoup(string, 'html.parser')

    return soup.find('html', recursive=False) is not None


def get_urls(soup: BeautifulSoup) -> Iterable[str]:
    for tag, attr in (
        ('a', 'href'),
        ('iframe', 'src'),
        ('img', 'src'),
        ('link', 'href'),
        ('script', 'src'),
    ):
        yield from (elm[attr] for elm in soup.find_all(tag) if elm.get(attr))


def get_sameorigin_urls(
    components: ParseResult,
    soup: BeautifulSoup,
) -> Iterable[str]:
    for url in get_urls(soup):
        url_c: ParseResult = urlparse(url)

        if (
            url_c.netloc == components.netloc and
            url_c.path.startswith(components.path)
        ):
            yield f'{url_c.scheme}://{url_c.netloc}{url_c.path}'
