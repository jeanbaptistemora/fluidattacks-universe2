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
    resolve,
    in_process,
)

# Local libraries
from lib_path.common import (
    blocking_get_vulnerabilities_from_iterator,
    EXTENSIONS_JAVA_PROPERTIES,
    SHIELD,
)
from parse_java_properties import (
    load as load_java_properties,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.model import (
    FindingEnum,
    Vulnerability,
)
from zone import (
    t,
)


def _java_properties_unencrypted_channel(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:

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

    return blocking_get_vulnerabilities_from_iterator(
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


@SHIELD
async def java_properties_unencrypted_channel(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _java_properties_unencrypted_channel,
        content=content,
        path=path,
    )


async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    store: EphemeralStore,
) -> None:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in EXTENSIONS_JAVA_PROPERTIES:
        coroutines.append(java_properties_unencrypted_channel(
            content=await content_generator(),
            path=path,
        ))

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
