from aioextensions import (
    in_process,
)
from lib_path.common import (
    SHIELD,
)
from lib_path.f346.android import (
    has_dangerous_permissions,
)
from model.core_model import (
    Vulnerabilities,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Awaitable,
    Callable,
    List,
)
from utils.function import (
    TIMEOUT_1MIN,
)


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def run_has_dangerous_permissions(
    content: str, path: str
) -> Vulnerabilities:
    return await in_process(
        has_dangerous_permissions,
        content=content,
        path=path,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], str],
    file_extension: str,
    file_name: str,
    path: str,
    **_: None,
) -> List[Awaitable[Vulnerabilities]]:
    coroutines: List[Awaitable[Vulnerabilities]] = []

    if (file_name, file_extension) == ("AndroidManifest", "xml"):
        coroutines.append(
            run_has_dangerous_permissions(content_generator(), path)
        )

    return coroutines
