from bs4 import (
    BeautifulSoup,
)
from bs4.element import (
    Tag,
)
from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from typing import (
    Iterator,
    Tuple,
)


def has_ssl_disabled(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        """
        Check if SSL is disabled in ``ApplicationHost.config``.

        Search for access tag in security section in an
        ``ApplicationHost.config`` source file or package.
        """
        soup = BeautifulSoup(content, features="html.parser")
        vulnerable: bool = True

        for custom_headers in soup("security"):
            for tag in custom_headers.contents:
                if isinstance(tag, Tag):
                    tag_name = tag.name
                    tag_value = tag.attrs.get("sslflags", "None")
                    if tag_name == "access" and tag_value != "None":
                        vulnerable = False
                    elif tag_name == "access" and tag_value == "None":
                        line_no: int = tag.sourceline
                        col_no: int = tag.sourcepos
                        yield line_no, col_no

        if vulnerable and soup("security"):
            line_no = 0
            col_no = 0
            yield line_no, col_no

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.dotnetconfig.has_ssl_disabled",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.DOTNETCONFIG_HAS_SSL_DISABLED,
    )
