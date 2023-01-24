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


def _json_anon_connection_config(
    template: Any,
) -> Iterator[Any]:
    if (
        isinstance(template, Node)
        and (hasattr(template.inner, "get"))
        and (allowed_hosts := template.inner.get("AllowedHosts"))
        and allowed_hosts.data == "*"
    ):
        yield allowed_hosts.start_line, allowed_hosts.start_column


def json_allowed_hosts(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f060.json_allowed_hosts",
        iterator=_json_anon_connection_config(
            template=template,
        ),
        path=path,
        method=MethodsEnum.JSON_ALLOWED_HOSTS,
    )
