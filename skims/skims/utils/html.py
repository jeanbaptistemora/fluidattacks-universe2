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
    # Check if it is a json file
    if string.startswith("{"):
        return False
    if soup is None:
        soup = BeautifulSoup(string, "html.parser")
    return soup.find("html", recursive=False) is not None


def _get_redirection_urls(soup: BeautifulSoup) -> Generator[str, None, None]:
    # Only use tags that could include redirections, not css, js, or jpg files
    for tag, attr in (("a", "href"), ("iframe", "src")):
        yield from (elm[attr] for elm in soup.find_all(tag) if elm.get(attr))


def get_sameorigin_urls(
    components: ParseResult,
    soup: BeautifulSoup,
) -> Generator[str, None, None]:
    for url in _get_redirection_urls(soup):
        url_c: ParseResult = urlparse(url)
        if (
            url_c.netloc == components.netloc
            and url_c.path.startswith(components.path)
            and not url_c.path.endswith((".css", ".js"))
        ):
            yield f"{url_c.scheme}://{url_c.netloc}{url_c.path}"


def get_alternative_protocol_urls(include_urls: set[str]) -> set[str]:
    urls: set[str] = set()
    urls.update(include_urls)
    http = "http://"
    https = "https://"
    for scope in include_urls:
        # FP: switch the type of protocol
        if scope.startswith(http):
            urls.add(scope.replace(http, https, 1))
        elif scope.startswith(https):
            urls.add(scope.replace(https, http, 1))

    return urls
