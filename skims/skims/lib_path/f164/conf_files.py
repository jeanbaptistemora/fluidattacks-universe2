from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from metaloaders.model import (
    Type as ModelType,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from typing import (
    Any,
    Iterator,
)


def _json_ssl_port_missing(
    template: Any,
) -> Iterator[Any]:
    if (
        (template.data_type == ModelType.OBJECT)
        and (conn_str := template.inner.get("iisSettings"))
        and (ii_express := conn_str.inner.get("iisExpress"))
        and (ssl_port := ii_express.inner.get("sslPort"))
        and ssl_port.data == 0
    ):
        yield ssl_port.start_line, ssl_port.start_column


def json_ssl_port_missing(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f164.json_ssl_port_missing",
        iterator=_json_ssl_port_missing(
            template=template,
        ),
        path=path,
        method=MethodsEnum.JSON_SSL_PORT_MISSING,
    )
