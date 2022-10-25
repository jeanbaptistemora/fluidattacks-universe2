# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f419.kubernetes import (
    k8s_check_audit_flag,
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
def run_k8s_check_audit_flag(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return k8s_check_audit_flag(content=content, path=path, template=template)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:

    results: Tuple[Vulnerabilities, ...] = ()

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        content = content_generator()
        for template in load_templates_blocking(content, fmt=file_extension):
            results = (
                *results,
                run_k8s_check_audit_flag(content, path, template),
            )
    return results
