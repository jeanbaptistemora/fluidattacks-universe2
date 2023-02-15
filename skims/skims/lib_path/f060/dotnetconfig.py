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
from typing import (
    Any,
)


def analyse_tags(custom_headers: Any) -> tuple[bool, int, int]:
    vulnerable: bool = True
    line_no: int = 0
    col_no: int = 0
    for tag in custom_headers.contents:
        if isinstance(tag, Tag):
            tag_name = tag.name
            tag_value = tag.attrs.get("sslflags", "None")
            if tag_name == "access" and tag_value != "None":
                vulnerable = False
            elif tag_name == "access" and tag_value == "None":
                line_no = tag.sourceline
                col_no = tag.sourcepos
    return (vulnerable, line_no, col_no)


def has_ssl_disabled(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        """
        Check if SSL is disabled in ``ApplicationHost.config``.

        Search for access tag in security section in an
        ``ApplicationHost.config`` source file or package.
        """
        soup = BeautifulSoup(content, features="html.parser")
        if soup("security"):
            vulnerable: bool = True
            line_no: int = 0
            col_no: int = 0

            for custom_headers in soup("security"):
                vuln_tag, line_no, col_no = analyse_tags(custom_headers)
                if not vuln_tag:
                    vulnerable = False

            if vulnerable:
                yield line_no, col_no

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.dotnetconfig.has_ssl_disabled",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.DOTNETCONFIG_HAS_SSL_DISABLED,
    )
