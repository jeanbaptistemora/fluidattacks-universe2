from lib_path.common import (
    EXTENSIONS_YAML,
    NAMES_DOCKERFILE,
    SHIELD_BLOCKING,
)
from lib_path.f266.docker import (
    container_whitout_user,
)
from model.core_model import (
    Vulnerabilities,
)
from re import (
    IGNORECASE,
    search,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Callable,
    Tuple,
)


@CACHE_ETERNALLY
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

    if (file_name in NAMES_DOCKERFILE and file_extension == "") or (
        search("docker", file_name, IGNORECASE)
        and file_extension in EXTENSIONS_YAML
    ):
        results = (run_container_whitout_user(content_generator(), path),)

    return results
