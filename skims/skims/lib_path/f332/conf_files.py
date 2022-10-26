# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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


def _json_check_https_argument(
    template: Any,
) -> Iterator[Any]:
    if isinstance(template, Node) and (
        scripts := template.inner.get("scripts").data
    ):
        for script in scripts.values():
            if (
                "react-scripts start" in script.data
                and "HTTPS=true" not in script.data
            ):
                yield script.start_line, script.start_column


def json_check_https_argument(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f332.json_check_https_argument",
        iterator=_json_check_https_argument(
            template=template,
        ),
        path=path,
        method=MethodsEnum.JSON_CHECK_HTTPS_ARGUMENT,
    )
