from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
    SHIELD,
)
from model import (
    core_model,
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
async def unverifiable_files(
    path: str,
    raw_content: bytes,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_iterator_blocking(
        content=raw_content.decode(encoding="utf-8", errors="replace"),
        cwe={"377"},
        description_key="src.lib_path.f117.unverifiable_files.description",
        finding=core_model.FindingEnum.F117,
        iterator=iter([(1, 0)]),
        path=path,
    )


@SHIELD
async def analyze(
    path: str,
    raw_content_generator: Callable[[], Awaitable[bytes]],
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = [
        unverifiable_files(
            path=path,
            raw_content=await raw_content_generator(),
        )
    ]

    return coroutines
