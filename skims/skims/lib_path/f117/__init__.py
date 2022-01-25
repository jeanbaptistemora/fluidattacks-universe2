from lib_path.common import (
    SHIELD,
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


@SHIELD
async def analyze(
    path: str,
    raw_content_generator: Callable[[], Awaitable[bytes]],
    **_: None,
) -> List[Awaitable[Vulnerabilities]]:

    coroutines: List[Awaitable[Vulnerabilities]] = [
        unverifiable_files(path, raw_content=await raw_content_generator())
    ]

    return coroutines
