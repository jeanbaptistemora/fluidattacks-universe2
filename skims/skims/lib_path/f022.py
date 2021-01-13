# Standard library
from typing import (
    Awaitable,
    Callable,
    Iterator,
    List,
    Tuple,
)

# Third party libraries
from aioextensions import (
    in_process,
)

# Local libraries
from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
    EXTENSIONS_JAVA_PROPERTIES,
    SHIELD,
)
from parse_java_properties import (
    load as load_java_properties,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from utils.function import (
    TIMEOUT_1MIN,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
from zone import (
    t,
)


def _java_properties_unencrypted_transport(
    content: str,
    path: str,
) -> Vulnerabilities:

    def iterator() -> Iterator[Tuple[int, int]]:
        data = load_java_properties(
            content,
            include_comments=False,
            exclude_protected_values=True,
        )
        for line_no, (key, val) in data.items():
            val = val.lower()
            if key and (
                val.startswith('http://')
                or val.startswith('ftp://')
            ) and not (
                'localhost' in val
                or '127.0.0.1' in val
                or '0.0.0.0' in val
            ):
                yield line_no, 0

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={'319'},
        description=t(
            key='src.lib_path.f022.unencrypted_channel',
            path=path,
        ),
        finding=FindingEnum.F022,
        iterator=iterator(),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def java_properties_unencrypted_transport(
    content: str,
    path: str,
) -> Vulnerabilities:
    return await in_process(
        _java_properties_unencrypted_transport,
        content=content,
        path=path,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[Vulnerabilities]]:
    coroutines: List[Awaitable[Vulnerabilities]] = []

    if file_extension in EXTENSIONS_JAVA_PROPERTIES:
        coroutines.append(java_properties_unencrypted_transport(
            content=await content_generator(),
            path=path,
        ))

    return coroutines
