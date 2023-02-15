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


def has_debug_enabled(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        """
        Check if debug flag is enabled in Web.config.

        Search for debug tag in compilation section in a Web.config source file
        or package.
        """
        soup = BeautifulSoup(content, features="html.parser")

        for custom_headers in soup("system.web"):
            for tag in custom_headers.contents:
                if isinstance(tag, Tag):
                    tag_name = tag.name
                    tag_value = tag.attrs.get("debug", "false")
                    if tag_name == "compilation" and tag_value == "true":
                        yield tag.sourceline, tag.sourcepos

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f183.dotnetconfig_has_debug_enabled",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.DOTNETCONFIG_HAS_DEBUG_ENABLED,
    )
