from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f117.generic import (
    unverifiable_files,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def analyze(
    path: str,
    raw_content_generator: Callable[[], bytes],
    **_: None,
) -> Tuple[Vulnerabilities, ...]:

    results: Tuple[Vulnerabilities, ...] = (
        unverifiable_files(path, raw_content=raw_content_generator()),
    )

    return results
