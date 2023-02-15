from bs4 import (
    BeautifulSoup,
)
from bs4.element import (
    Tag,
)
from collections.abc import (
    Iterator,
)
from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)


def has_remove_banner(soup: BeautifulSoup) -> bool:
    for custom_headers in soup("customHeaders"):
        for tag in custom_headers.contents:
            if isinstance(tag, Tag):
                tag_name = tag.name
                tag_value = tag.attrs.get("name")
                if tag_name == "remove" and tag_value == "X-Powered-By":
                    return True
    return False


def not_suppress_vuln_header(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        """
        Search for X-Powered-By headers in a Web.config source file or package.
        """
        soup = BeautifulSoup(content, features="xml")
        if soup("customHeaders") and not has_remove_banner(soup):
            line_no: int = 0
            col_no: int = 0
            yield line_no, col_no

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.dotnetconfig.not_suppress_vuln_header",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.DOTNETCONFIG_NOT_SUPPRESS_VULN_HEADER,
    )
