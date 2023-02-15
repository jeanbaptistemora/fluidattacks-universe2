from collections.abc import (
    Callable,
)
from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f037.dotnetconfig import (
    not_suppress_vuln_header,
)
from model.core_model import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_not_suppress_vuln_header(content: str, path: str) -> Vulnerabilities:
    return not_suppress_vuln_header(content=content, path=path)


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
            run_not_suppress_vuln_header(content_generator(), path),
        )

    return results
