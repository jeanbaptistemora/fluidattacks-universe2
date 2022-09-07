# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f065.html import (
    has_autocomplete,
    is_cacheable,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_is_cacheable(content: str, path: str) -> Vulnerabilities:
    return is_cacheable(content=content, path=path)


@SHIELD_BLOCKING
def run_has_autocomplete(content: str, path: str) -> Vulnerabilities:
    return has_autocomplete(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()

    if file_extension == "html":
        results = (
            *results,
            run_has_autocomplete(content_generator(), path),
            run_is_cacheable(content_generator(), path),
        )

    return results
