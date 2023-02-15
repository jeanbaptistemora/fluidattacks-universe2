from collections.abc import (
    Callable,
)
from lib_path.common import (
    EXTENSIONS_YAML,
    NAMES_DOCKERFILE,
    SHIELD_BLOCKING,
)
from lib_path.f418.docker import (
    docker_compose_read_only,
    docker_using_add_command,
)
from model.core_model import (
    Vulnerabilities,
)
from parse_cfn.loader import (
    load_templates_blocking,
)
from typing import (
    Any,
)


@SHIELD_BLOCKING
def run_docker_compose_read_only(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return docker_compose_read_only(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def run_docker_using_add_command(
    content: str,
    path: str,
) -> Vulnerabilities:
    return docker_using_add_command(
        content=content,
        path=path,
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    file_name: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:

    results: tuple[Vulnerabilities, ...] = ()
    content = content_generator()

    if "docker" in file_name.lower() and file_extension in EXTENSIONS_YAML:
        results = (
            *results,
            *(
                run_docker_compose_read_only(content, path, template)
                for template in load_templates_blocking(
                    content, fmt=file_extension
                )
            ),
        )
    elif file_name in NAMES_DOCKERFILE:
        results = (
            *results,
            run_docker_using_add_command(content, path),
        )
    return results
