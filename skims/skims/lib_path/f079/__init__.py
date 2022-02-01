from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f079.generic import (
    non_upgradeable_deps,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Awaitable,
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def analyze(
    path: str,
    raw_content_generator: Callable[[], Awaitable[bytes]],
    **_: None,
) -> Tuple[Vulnerabilities, ...]:

    results: Tuple[Vulnerabilities, ...] = (
        non_upgradeable_deps(path, raw_content_generator()),
    )

    return results
