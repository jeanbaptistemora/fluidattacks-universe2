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
    Iterator,
    Tuple,
)


def jmx_header_basic(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:

        soup = BeautifulSoup(content, features="html.parser")
        for tag in soup.find_all("stringprop"):
            if isinstance(tag, Tag):
                tag_name = tag.name
                tag_attrs = tag.attrs
                tag_content = str(tag).lower()
                if (
                    (name_attr := tag_attrs.get("name"))
                    and name_attr.lower() == "header.value"
                    and tag_name == "stringprop"
                    and re.search(r">basic\b", tag_content)
                ):
                    line_no: int = tag.sourceline
                    col_no: int = tag.sourcepos
                    yield line_no, col_no

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f015.jmx_header_basic",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.JMX_HEADER_BASIC,
    )


def basic_auth_method(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
        """
        Search for a Basic auth method in a config file.
        """
        soup = BeautifulSoup(content, features="html.parser")
        for tag in soup.find_all("auth-method"):
            if isinstance(tag, Tag):
                tag_name = tag.name
                tag_content = str(tag.string).lower()
                if tag_name == "auth-method" and re.search(
                    r"\bbasic\b", tag_content
                ):
                    line_no: int = tag.sourceline
                    col_no: int = tag.sourcepos
                    yield line_no, col_no

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f015.basic_auth_method",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.XML_BASIC_AUTH_METHOD,
    )
