from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f066.javascript import (
    uses_console_log,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_uses_console_log(content: str, path: str) -> Vulnerabilities:
    return uses_console_log(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()

    if file_extension in ("js", "ts"):
        results = (
            *results,
            run_uses_console_log(content_generator(), path),
        )

    return results
