from collections.abc import (
    Callable,
)
from lib_path.common import (
    NAMES_DOCKERFILE,
    SHIELD_BLOCKING,
)
from lib_path.f266.docker import (
    container_with_user_root,
    container_without_user,
    docker_compose_without_user,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Any,
)


@SHIELD_BLOCKING
def run_container_without_user(content: str, path: str) -> Vulnerabilities:
    return container_without_user(content=content, path=path)


@SHIELD_BLOCKING
def run_docker_compose_without_user(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return docker_compose_without_user(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_container_with_user_root(content: str, path: str) -> Vulnerabilities:
    return container_with_user_root(content=content, path=path)


def analyze(
    content_generator: Callable[[], str],
    file_name: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    content = content_generator()

    if file_name in NAMES_DOCKERFILE:
        results = (
            *results,
            run_container_without_user(content, path),
            run_container_with_user_root(content, path),
        )

    return results
