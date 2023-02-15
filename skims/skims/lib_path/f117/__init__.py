from collections.abc import (
    Callable,
)
from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f117.generic import (
    unverifiable_files,
)
from model.core_model import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def analyze(
    path: str,
    raw_content_generator: Callable[[], bytes],
    **_: None,
) -> tuple[Vulnerabilities, ...]:

    results: tuple[Vulnerabilities, ...] = (
        unverifiable_files(path, raw_content=raw_content_generator()),
    )

    return results
