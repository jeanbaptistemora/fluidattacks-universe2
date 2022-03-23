from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
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
    connection_str = template.inner.get("iisSettings")
    if (
        connection_str
        and (
            anon_connect := connection_str.inner.get("anonymousAuthentication")
        )
        and anon_connect.data
    ):
        yield anon_connect.start_line, anon_connect.start_column


def json_anon_connection_config(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f056.json_anon_connection_config",
        iterator=_json_anon_connection_config(
            template=template,
        ),
        path=path,
        method=MethodsEnum.JSON_ANON_CONNECTION_CONFIG,
    )
