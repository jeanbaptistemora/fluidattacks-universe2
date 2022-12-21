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
import re
from typing import (
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
)


def parse_tag(a_href: Tag) -> Dict[str, Optional[str]]:
    parsed: dict = {
        "href": a_href.get("href"),
        "target": a_href.get("target"),
        "rel": a_href.get("rel"),
    }

    for key, value in parsed.items():
        if isinstance(value, List):
            parsed.update({key: " ".join(value)})

    return parsed


def has_reverse_tabnabbing(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        http_re = re.compile(r"^http(s)?://|^\{.*\}")
        rel_re = re.compile(r"(?=.*noopener)(?=.*noreferrer)")
        html_obj = BeautifulSoup(content, features="html.parser")

        for a_href in html_obj.findAll("a", attrs={"href": http_re}):
            parsed: Dict[str, Optional[str]] = parse_tag(a_href)

            if (
                parsed["href"]
                and parsed["target"] == "_blank"
                and (not parsed["rel"] or not rel_re.match(parsed["rel"]))
            ):
                yield a_href.sourceline, a_href.sourcepos

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f097.has_reverse_tabnabbing",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.HTML_HAS_REVERSE_TABNABBING,
    )
