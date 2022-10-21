# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f164.conf_files import (
    json_ssl_port_missing,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_blocking,
)
from typing import (
    Any,
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_json_ssl_port_missing(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return json_ssl_port_missing(content=content, path=path, template=template)


def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:

    content = content_generator()
    results: Tuple[Vulnerabilities, ...] = ()

    if file_extension == "json":
        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                run_json_ssl_port_missing(content, path, template),
            )
    return results
