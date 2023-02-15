from bs4 import (
    BeautifulSoup,
)
from collections.abc import (
    Generator,
)
from string import (
    whitespace,
)
from urllib.parse import (
    ParseResult,
    urlparse,
)


def is_html(string: str, soup: BeautifulSoup | None = None) -> bool:
    string = string.strip(whitespace)

    if string.startswith("{"):
        # JSON
        return False

    if soup is None:
        soup = BeautifulSoup(string, "html.parser")

    return soup.find("html", recursive=False) is not None


def get_urls(soup: BeautifulSoup) -> Generator[str, None, None]:
    for tag, attr in (
        ("a", "href"),
        ("iframe", "src"),
        ("img", "src"),
        ("link", "href"),
        ("script", "src"),
    ):
        yield from (elm[attr] for elm in soup.find_all(tag) if elm.get(attr))


def get_sameorigin_urls(
    components: ParseResult,
    soup: BeautifulSoup,
) -> Generator[str, None, None]:
    for url in get_urls(soup):
        url_c: ParseResult = urlparse(url)

        if url_c.netloc == components.netloc and url_c.path.startswith(
            components.path
        ):
            yield f"{url_c.scheme}://{url_c.netloc}{url_c.path}"
