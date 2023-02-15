from collections.abc import (
    Callable,
)
from lib_path.common import (
    EXTENSIONS_BASH,
    EXTENSIONS_YAML,
    NAMES_DOCKERFILE,
    SHIELD_BLOCKING,
)
from lib_path.f380.bash import (
    image_has_digest,
)
from lib_path.f380.docker import (
    docker_compose_image_has_digest,
    unpinned_docker_image,
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


@SHIELD_BLOCKING
def run_unpinned_docker_image(content: str, path: str) -> Vulnerabilities:
    return unpinned_docker_image(content=content, path=path)


@SHIELD_BLOCKING
def run_image_has_digest(content: str, path: str) -> Vulnerabilities:
    return image_has_digest(content=content, path=path)


@SHIELD_BLOCKING
def run_docker_compose_image_has_digest(
    content: str, path: str, template: Node
) -> Vulnerabilities:
    return docker_compose_image_has_digest(
        content=content, path=path, template=template
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

    if file_extension in EXTENSIONS_BASH:
        results = (run_image_has_digest(content, path),)

    if file_name in NAMES_DOCKERFILE:
        results = (run_unpinned_docker_image(content, path),)

    if "docker" in file_name.lower() and file_extension in EXTENSIONS_YAML:
        results = (
            *results,
            *(
                run_docker_compose_image_has_digest(content, path, template)
                for template in load_templates_blocking(
                    content, fmt=file_extension
                )
            ),
        )
    return results
