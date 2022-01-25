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
    List,
)


@SHIELD_BLOCKING
def analyze(
    path: str,
    raw_content_generator: Callable[[], Awaitable[bytes]],
    **_: None,
) -> List[Awaitable[Vulnerabilities]]:

    coroutines: List[Awaitable[Vulnerabilities]] = [
        non_upgradeable_deps(path, raw_content_generator())
    ]

    return coroutines
