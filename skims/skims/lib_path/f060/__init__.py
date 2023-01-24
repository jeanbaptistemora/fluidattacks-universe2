from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f060.dotnetconfig import (
    has_ssl_disabled,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_has_ssl_disabled(content: str, path: str) -> Vulnerabilities:
    return has_ssl_disabled(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()
    content = content_generator()

    if file_extension == "config":
        results = (
            *results,
            run_has_ssl_disabled(content, path),
        )

    return results
