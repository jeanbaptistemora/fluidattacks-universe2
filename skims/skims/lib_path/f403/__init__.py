# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f403.conf_files import (
    insecure_configuration,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_has_x_xss_protection_header(
    content: str, path: str
) -> Vulnerabilities:
    return insecure_configuration(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()

    if file_extension == "xml":
        results = (
            *results,
            run_has_x_xss_protection_header(content_generator(), path),
        )

    return results
