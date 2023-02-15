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


def has_x_xss_protection_header(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        soup = BeautifulSoup(content, features="html.parser")

        for tag in soup.find_all("add"):
            if (
                isinstance(tag, Tag)
                and tag.name == "add"
                and (tag_value := tag.attrs.get("name"))
                and tag_value.lower() == "x-xss-protection"
            ):
                line_no: int = tag.sourceline
                col_no: int = tag.sourcepos
                yield line_no, col_no

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.conf_files.has_x_xss_protection_header",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.XML_HAS_X_XSS_PROTECTION_HEADER,
    )
