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


def _find_parent(tag: Tag) -> bool:
    if tag.find_parent(name="cross-domain-policy"):
        return True
    return False


def allow_acces_from_any_domain(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        soup = BeautifulSoup(content, features="html.parser")

        for tag in soup.find_all("allow-acces-from"):
            if (
                isinstance(tag, Tag)
                and tag.name == "allow-acces-from"
                and (tag_value := tag.attrs.get("domain"))
                and tag_value.lower() == "*"
                and _find_parent(tag)
            ):
                line_no: int = tag.sourceline
                col_no: int = tag.sourcepos
                yield line_no, col_no

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_root.f060.xml_allowed_domains",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.XML_ALLOWS_ALL_DOMAINS,
    )
