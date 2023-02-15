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


def not_custom_errors(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        """
        Check if customErrors flag is set to off in Web.config.

        CWE-12: ASP.NET Misconfiguration: Missing Custom Error Page

        """
        soup = BeautifulSoup(content, features="html.parser")

        for custom_headers in soup("system.web"):
            for tag in custom_headers.contents:
                if isinstance(tag, Tag):
                    tag_name = tag.name
                    tag_value = tag.attrs.get("mode", "RemoteOnly")
                    if tag_name == "customerrors" and tag_value == "Off":
                        yield tag.sourceline, tag.sourcepos

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f239.dotnetconfig_not_custom_errors",
        iterator=iterator(),
        path=path,
        method=MethodsEnum.DOTNETCONFIG_NOT_CUSTOM_ERRORS,
    )
