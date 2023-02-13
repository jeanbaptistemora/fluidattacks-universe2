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


def header_allow_all_methods(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        soup = BeautifulSoup(content, features="html.parser")

        for tag in soup.find_all("add"):
            if (
                isinstance(tag, Tag)
                and tag.name == "add"
                and (tag_value := tag.attrs.get("verb"))
                and tag_value.lower() == "*"
            ):
                line_no: int = tag.sourceline
                col_no: int = tag.sourcepos
                yield line_no, col_no

    desc = "src.lib_path.f044.severless_bucket_has_https_methos_enabled"
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=desc,
        iterator=iterator(),
        path=path,
        method=MethodsEnum.XML_HEADER_ALLOW_ALL_METHODS,
    )
