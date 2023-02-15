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


def xml_x_frame_options(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        """
        Search for X-Frame-Options headers in
        a Web.config source file or package.
        """
        soup = BeautifulSoup(content, features="html.parser")

        for tag in soup.find_all("add"):
            if (
                isinstance(tag, Tag)
                and tag.name == "add"
                and (tag_value := tag.attrs.get("name"))
                and tag_value.lower() == "x-frame-options"
            ):
                line_no: int = tag.sourceline
                col_no: int = tag.sourcepos
                yield line_no, col_no

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f152.xml_x_frame_options",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.XML_X_FRAME_OPTIONS,
    )
