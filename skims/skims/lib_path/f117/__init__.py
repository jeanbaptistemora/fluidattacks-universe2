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
    Awaitable,
    Callable,
    List,
)


@SHIELD_BLOCKING
def analyze(
    path: str,
    raw_content_generator: Callable[[], bytes],
    **_: None,
) -> List[Vulnerabilities]:

    coroutines: List[Awaitable[Vulnerabilities]] = [
        unverifiable_files(path, raw_content=raw_content_generator())
    ]

    return coroutines
