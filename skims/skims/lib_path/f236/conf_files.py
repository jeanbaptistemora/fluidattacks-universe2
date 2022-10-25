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


def _json_sourcemap_in_build(
    template: Any,
) -> Iterator[Any]:
    if isinstance(template, Node) and (
        scripts := template.inner.get("scripts").data
    ):
        for script in scripts.values():
            if (
                " react-scripts build" in script.data
                and " GENERATE_SOURCEMAP=false" not in script.data
            ):
                yield script.start_line, script.start_column


def json_sourcemap_in_build(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        description_key="lib_path.f236.json_sourcemap_in_build",
        iterator=_json_sourcemap_in_build(
            template=template,
        ),
        path=path,
        method=MethodsEnum.JSON_SOURCEMAP_IN_BUILD,
    )
