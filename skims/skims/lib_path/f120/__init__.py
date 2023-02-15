from collections.abc import (
    Callable,
)
from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f120.python import (
    pip_incomplete_dependencies_list,
)
from model.core_model import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_pip_incomplete_dependencies_list(
    content: str, path: str
) -> Vulnerabilities:
    return pip_incomplete_dependencies_list(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    path: str,
    content_generator: Callable[[], str],
    file_extension: str,
    file_name: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    if (file_name, file_extension) == ("requirements", "txt"):
        results = (
            *results,
            run_pip_incomplete_dependencies_list(content_generator(), path),
        )

    return results
