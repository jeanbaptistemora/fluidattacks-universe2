# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    EXTENSIONS_JSON,
    EXTENSIONS_YAML,
    SHIELD_BLOCKING,
)
from lib_path.f332.conf_files import (
    json_check_https_argument,
)
from lib_path.f332.kubernetes import (
    kubernetes_insecure_port,
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
def run_kubernetes_insecure_port(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return kubernetes_insecure_port(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_json_check_https_argument(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return json_check_https_argument(
        content=content, path=path, template=template
    )


def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()

    if file_extension in EXTENSIONS_YAML:
        content = content_generator()

        results = (
            *results,
            *(
                run_kubernetes_insecure_port(content, path, template)
                for template in load_templates_blocking(
                    content, fmt=file_extension
                )
            ),
        )
    elif file_extension in EXTENSIONS_JSON:
        content = content_generator()

        results = (
            *results,
            *(
                run_json_check_https_argument(content, path, template)
                for template in load_templates_blocking(
                    content, fmt=file_extension
                )
            ),
        )
    return results
