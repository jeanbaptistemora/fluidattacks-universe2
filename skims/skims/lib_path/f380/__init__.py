# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_path.common import (
    EXTENSIONS_BASH,
    NAMES_DOCKERFILE,
    SHIELD_BLOCKING,
)
from lib_path.f380.bash import (
    image_has_digest,
)
from lib_path.f380.docker import (
    unpinned_docker_image,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_unpinned_docker_image(content: str, path: str) -> Vulnerabilities:
    return unpinned_docker_image(content=content, path=path)


@SHIELD_BLOCKING
def run_image_has_digest(content: str, path: str) -> Vulnerabilities:
    return image_has_digest(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    file_name: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()

    if file_extension in EXTENSIONS_BASH:
        results = (run_image_has_digest(content_generator(), path),)

    if file_name in NAMES_DOCKERFILE:
        results = (run_unpinned_docker_image(content_generator(), path),)

    return results
