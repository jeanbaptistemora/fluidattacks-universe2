from bs4 import (
    BeautifulSoup,
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


def has_not_subresource_integrity(content: str, path: str) -> Vulnerabilities:
    def iterator() -> Iterator[tuple[int, int]]:
        r"""
        Check if elements fetched by the provided HTML have `SRI`.

        See: `Documentation <https://developer.mozilla.org/en-US/
        docs/Web/Security/Subresource_Integrity>`_.

        :param path: Path to the ``HTML`` source.
        :rtype: :class:`fluidasserts.Result`
        """

        soup = BeautifulSoup(content, features="html.parser")

        for elem_types in ("link", "script"):
            for elem in soup(elem_types):
                does_not_have_integrity: bool = elem.get("integrity") is None

                if elem_types == "link":
                    references_external_resource: bool = elem.get(
                        "href", ""
                    ).startswith("http")
                elif elem_types == "script":
                    references_external_resource = elem.get(
                        "src", ""
                    ).startswith("http")

                if does_not_have_integrity and references_external_resource:
                    yield elem.sourceline, elem.sourcepos

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key=(
            "lib_path.f086.sub_resource_integrity.missing_integrity"
        ),
        iterator=iterator(),
        path=path,
        method=MethodsEnum.HTML_HAS_NOT_SUB_RESOURCE_INTEGRITY,
    )
