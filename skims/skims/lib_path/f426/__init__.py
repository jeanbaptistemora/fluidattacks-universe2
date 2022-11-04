# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    EXTENSIONS_CLOUDFORMATION,
    SHIELD_BLOCKING,
)
from lib_path.f426.kubernetes import (
    k8s_image_has_digest,
)
from metaloaders.model import (
    Node,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_blocking,
)
from typing import (
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_k8s_image_has_digest(
    content: str, path: str, template: Node
) -> Vulnerabilities:
    return k8s_image_has_digest(content=content, path=path, template=template)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:

    results: Tuple[Vulnerabilities, ...] = ()
    content = content_generator()

    if file_extension in EXTENSIONS_CLOUDFORMATION:
        results = (
            *results,
            *(
                run_k8s_image_has_digest(content, path, template)
                for template in load_templates_blocking(
                    content, fmt=file_extension
                )
            ),
        )
    return results
