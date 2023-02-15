from collections.abc import (
    Callable,
)
from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f371.html import (
    is_header_content_type_missing,
)
from model.core_model import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_is_header_content_type_missing(
    content: str, path: str
) -> Vulnerabilities:
    return is_header_content_type_missing(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    if file_extension == "html":
        results = (
            *results,
            run_is_header_content_type_missing(content_generator(), path),
        )

    return results
