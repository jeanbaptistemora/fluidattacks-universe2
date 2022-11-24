from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from typing import (
    Any,
    Iterator,
)


def _json_principal_wildcard(
    template: Any,
) -> Iterator[Any]:
    if isinstance(template, Node) and (
        statement := template.inner.get("Statement")
    ):
        for elem in statement.data:
            if (
                isinstance(elem, Node)
                and (principal := elem.inner.get("Principal"))
                and isinstance(principal, Node)
                and principal.data == "*"
            ):
                yield principal.start_line, principal.start_column


def json_principal_wildcard(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f325.json_principal_wildcard",
        iterator=_json_principal_wildcard(
            template=template,
        ),
        path=path,
        method=MethodsEnum.JSON_PRINCIPAL_WILDCARD,
    )
