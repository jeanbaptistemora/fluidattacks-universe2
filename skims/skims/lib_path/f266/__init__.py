from lib_path.common import (
    EXTENSIONS_DOCKERFILE,
    NAMES_DOCKERFILE,
    SHIELD_BLOCKING,
)
from lib_path.f266.docker import (
    container_whitout_user,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_container_whitout_user(content: str, path: str) -> Vulnerabilities:
    return container_whitout_user(content=content, path=path)


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

    return results
