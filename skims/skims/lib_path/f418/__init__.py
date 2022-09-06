from lib_path.common import (
    EXTENSIONS_YAML,
    SHIELD_BLOCKING,
)
from lib_path.f418.docker import (
    docker_compose_read_only,
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
def run_docker_compose_read_only(
    content: str, path: str, template: Any
) -> Vulnerabilities:
    return docker_compose_read_only(
        content=content, path=path, template=template
    )


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    file_name: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()

    if "docker" in file_name.lower() and file_extension in EXTENSIONS_YAML:
        content = content_generator()
        results = (
            *results,
            *(
                run_docker_compose_read_only(content, path, template)
                for template in load_templates_blocking(
                    content, fmt=file_extension
                )
            ),
        )

    return results
