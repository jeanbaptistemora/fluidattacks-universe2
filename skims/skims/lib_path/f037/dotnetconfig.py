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


def has_remove_banner(custom_headers: Tag) -> bool:
    for header in custom_headers.find_all("remove"):
        if (header_name := header.attrs.get("name")) and (
            header_name.lower() == "x-powered-by"
        ):
            return True
    return False


def not_suppress_vuln_header(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        soup = BeautifulSoup(content, features="html.parser")
        for tag in soup.find_all("customheaders"):
            if isinstance(tag, Tag) and not has_remove_banner(tag):
                line_no: int = tag.sourceline
                col_no: int = 0
                yield line_no, col_no

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.dotnetconfig.not_suppress_vuln_header",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.DOTNETCONFIG_NOT_SUPPRESS_VULN_HEADER,
    )
