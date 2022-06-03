from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f065.html import (
    has_not_autocomplete,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Tuple,
)


@SHIELD_BLOCKING
def run_has_not_autocomplete(path: str) -> Vulnerabilities:
    return has_not_autocomplete(path)


@SHIELD_BLOCKING
def analyze(
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:
    results: Tuple[Vulnerabilities, ...] = ()

    if file_extension == "html":
        results = (run_has_not_autocomplete(path),)

    return results
