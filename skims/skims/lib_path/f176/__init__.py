from collections.abc import (
    Callable,
)
from lib_path.common import (
    EXTENSIONS_BASH,
    EXTENSIONS_YAML,
    NAMES_DOCKERFILE,
    SHIELD_BLOCKING,
)
from lib_path.f176.bash import (
    bash_using_sshpass,
)
from lib_path.f176.docker import (
    container_using_sshpass,
)
from model.core_model import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_container_using_sshpass(content: str, path: str) -> Vulnerabilities:
    return container_using_sshpass(content=content, path=path)


@SHIELD_BLOCKING
def run_bash_using_sshpass(content: str, path: str) -> Vulnerabilities:
    return bash_using_sshpass(content=content, path=path)


def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    file_name: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    if (file_name in NAMES_DOCKERFILE) or (
        "docker" in file_name.lower() and file_extension in EXTENSIONS_YAML
    ):
        results = (run_container_using_sshpass(content_generator(), path),)
    elif file_extension in EXTENSIONS_BASH:
        results = (
            *results,
            run_bash_using_sshpass(content_generator(), path),
        )
    return results
