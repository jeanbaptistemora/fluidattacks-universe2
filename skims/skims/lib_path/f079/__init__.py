# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f079.generic import (
    non_upgradeable_deps,
)
from lib_path.f079.python import (
    pip_incomplete_dependencies_list,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_pip_incomplete_dependencies_list(
    content: str, path: str
) -> Vulnerabilities:
    return pip_incomplete_dependencies_list(content=content, path=path)


@SHIELD_BLOCKING
def run_non_upgradeable_deps(path: str, raw_content: bytes) -> Vulnerabilities:
    return non_upgradeable_deps(path=path, raw_content=raw_content)


@SHIELD_BLOCKING
def analyze(  # pylint: disable=too-many-arguments
    path: str,
    raw_content_generator: Callable[[], bytes],
    content_generator: Callable[[], str],
    file_extension: str,
    file_name: str,
    unique_nu_paths: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()

    if path in unique_nu_paths:
        results = (
            *results,
            run_non_upgradeable_deps(path, raw_content_generator()),
        )

    if (file_name, file_extension) == ("requirements", "txt"):
        results = (
            *results,
            run_pip_incomplete_dependencies_list(content_generator(), path),
        )

    return results
