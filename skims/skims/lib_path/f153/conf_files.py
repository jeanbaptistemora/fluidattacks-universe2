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


def _eval_header(tag: Tag) -> bool:
    if (
        tag.name == "stringprop"
        and (tag_value := tag.attrs.get("name"))
        and tag_value.lower() == "header.name"
        and (tag_content := str(tag.string).lower())
        and tag_content == "accept"
    ):
        return True
    return False


def _next_sibling(tag: Tag) -> bool:
    if (
        (
            next_tag := tag.find_next_sibling(
                name="stringprop",
                text="*/*",
            )
        )
        and (tag_value := next_tag.attrs.get("name"))
        and tag_value.lower() == "header.value"
    ):
        return True
    return False


def xml_accept_header(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        """
        Search for Accept headers with wildcard value in
        a Web.config source file or package.
        """
        soup = BeautifulSoup(content, features="html.parser")
        for tag in soup.find_all("stringprop"):
            if _eval_header(tag) and _next_sibling(tag):
                line_no: int = tag.sourceline
                col_no: int = tag.sourcepos
                yield line_no, col_no

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f153.xml_accept_header",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.XML_ACCEPT_HEADER,
    )
