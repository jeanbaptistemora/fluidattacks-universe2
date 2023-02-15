from collections.abc import (
    Callable,
)
from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f405.bash import (
    excessive_privileges_for_others,
)
from model.core_model import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_excessive_privileges_for_others(
    content: str, path: str
) -> Vulnerabilities:
    return excessive_privileges_for_others(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    file_name: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    results: tuple[Vulnerabilities, ...] = ()

    if file_extension in ("sh", "com") or file_name == "Dockerfile":
        results = (
            *results,
            run_excessive_privileges_for_others(content_generator(), path),
        )

    return results
