from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f065.html import (
    has_autocomplete,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_has_autocomplete(content: str, path: str) -> Vulnerabilities:
    return has_autocomplete(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()

    if file_extension == "html":
        results = (run_has_autocomplete(content_generator(), path),)

    return results
