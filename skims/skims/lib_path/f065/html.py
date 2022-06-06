from bs4 import (
    BeautifulSoup,
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


def has_autocomplete(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[Tuple[int, int]]:
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
        method=MethodsEnum.HAS_AUTOCOMPLETE,
    )
