from lib_path.common import (
    SHIELD_BLOCKING,
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


@CACHE_ETERNALLY
@SHIELD_BLOCKING
def run_has_dangerous_permissions(content: str, path: str) -> Vulnerabilities:
    return has_dangerous_permissions(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
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
