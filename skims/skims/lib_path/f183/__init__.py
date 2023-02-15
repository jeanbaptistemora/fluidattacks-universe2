from collections.abc import (
    Callable,
)
from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f183.dotnetconfig import (
    has_debug_enabled,
)
from model.core_model import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_has_debug_enabled(content: str, path: str) -> Vulnerabilities:
    return has_debug_enabled(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    if file_extension == "config":
        results = (
            *results,
            run_has_debug_enabled(content_generator(), path),
        )

    return results
