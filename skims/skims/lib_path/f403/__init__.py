from collections.abc import (
    Callable,
)
from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f403.conf_files import (
    insecure_configuration,
)
from model.core_model import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_has_x_xss_protection_header(
    content: str, path: str
) -> Vulnerabilities:
    return insecure_configuration(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    if file_extension == "xml":
        results = (
            *results,
            run_has_x_xss_protection_header(content_generator(), path),
        )

    return results
