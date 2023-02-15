from bs4 import (
    BeautifulSoup,
)
from collections.abc import (
    Iterator,
)
from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
    has_attributes,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from pyparsing import (
    CaselessKeyword,
)


def has_autocomplete(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        """
        Check if *input* or *form* tags have *autocomplete*
        attribute set to *off*.

        It's known that *form* tags may have the *autocomplete* attribute set
        to *on* and specific *input* tags have it set to *off*. However, this
        check enforces a defensive and explicit approach,
        forcing every *input* and *form* tag to have the *autocomplete*
        attribute set to *off*.
        """

        html_obj = BeautifulSoup(content, features="html.parser")

        for obj in html_obj("input"):
            autocomplete_enabled: bool = obj.get("autocomplete", "on") != "off"
            is_input_enabled: bool = obj.get("disabled") != ""
            is_input_type_sensitive: bool = obj.get("type", "text") in (
                # autocomplete only works with these:
                #   https://www.w3schools.com/tags/att_input_autocomplete.asp
                "checkbox",
                "date",
                "datetime-local",
                "email",
                "month",
                "password",
                "search",
                "tel",
                "text",
                "time",
                "url",
                "week",
            )
            if (
                autocomplete_enabled
                and is_input_type_sensitive
                and is_input_enabled
            ):
                yield obj.sourceline, obj.sourcepos

        for obj in html_obj("form"):
            if obj.attrs.get("autocomplete", "on") != "off":
                yield obj.sourceline, obj.sourcepos

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f065.has_autocomplete",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.HTML_HAS_AUTOCOMPLETE,
    )


def is_cacheable(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        """Check if cache is possible.

        Verifies if the file has the tags::
        <META HTTP-EQUIV="Pragma" CONTENT="no-cache"> and
        <META HTTP-EQUIV="Expires" CONTENT="-1"
        """

        tag = "meta"
        tk_pragma = CaselessKeyword("pragma")
        tk_nocache = CaselessKeyword("no-cache")
        pragma_attrs = {"http-equiv": tk_pragma, "content": tk_nocache}

        tk_expires = CaselessKeyword("expires")
        tk_minusone = CaselessKeyword("-1")
        expires_attrs = {"http-equiv": tk_expires, "content": tk_minusone}

        has_pragma = has_attributes(content, tag, pragma_attrs)
        has_expires = has_attributes(content, tag, expires_attrs)

        vulnerable: bool = not has_pragma or not has_expires
        if vulnerable:
            line: int = 0
            column: int = 0
            yield line, column

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f065.is_cacheable",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.HTML_IS_CACHEABLE,
    )
