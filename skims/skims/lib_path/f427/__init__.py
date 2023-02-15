from collections.abc import (
    Callable,
)
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
) -> tuple[Vulnerabilities, ...]:

    results: tuple[Vulnerabilities, ...] = ()
    content = content_generator()

    if file_name in NAMES_DOCKERFILE:
        results = (
            *results,
            run_docker_port_exposed(content, path),
        )
    return results
