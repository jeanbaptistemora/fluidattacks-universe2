# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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


def _json_anon_connection_config(
    template: Any,
) -> Iterator[Any]:
    if (
        template.data_type == ModelType.OBJECT
        and (conn_str := template.inner.get("iisSettings"))
        and (anon_conn := conn_str.inner.get("anonymousAuthentication"))
        and anon_conn.data
    ):
        yield anon_conn.start_line, anon_conn.start_column


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
