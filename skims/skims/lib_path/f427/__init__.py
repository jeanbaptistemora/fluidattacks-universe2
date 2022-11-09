# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    NAMES_DOCKERFILE,
    SHIELD_BLOCKING,
)
from lib_path.f427.docker import (
    docker_port_exposed,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_docker_port_exposed(
    content: str,
    path: str,
) -> Vulnerabilities:
    return docker_port_exposed(
        content=content,
        path=path,
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_name: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:

    results: Tuple[Vulnerabilities, ...] = ()
    content = content_generator()

    if file_name in NAMES_DOCKERFILE:
        results = (
            *results,
            run_docker_port_exposed(content, path),
        )
    return results
