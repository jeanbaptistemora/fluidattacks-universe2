# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    EXTENSIONS_DOCKERFILE,
    EXTENSIONS_YAML,
    NAMES_DOCKERFILE,
    SHIELD_BLOCKING,
)
from lib_path.f266.docker import (
    container_whitout_user,
    docker_compose_whitout_user,
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
def run_container_whitout_user(content: str, path: str) -> Vulnerabilities:
    return container_whitout_user(content=content, path=path)


@SHIELD_BLOCKING
def run_docker_compose_whitout_user(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return docker_compose_whitout_user(
        content=content, path=path, template=template
    )


def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    file_name: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()

    if (
        file_name in NAMES_DOCKERFILE
        and file_extension in EXTENSIONS_DOCKERFILE
    ):
        results = (run_container_whitout_user(content_generator(), path),)

    if "docker" in file_name.lower() and file_extension in EXTENSIONS_YAML:
        content = content_generator()
        results = (
            *results,
            *(
                run_docker_compose_whitout_user(content, path, template)
                for template in load_templates_blocking(
                    content, fmt=file_extension
                )
            ),
        )
    return results
