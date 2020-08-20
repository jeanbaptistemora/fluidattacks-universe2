# Standard library
from typing import (
    Awaitable,
    Callable,
    List,
    Set,
    Tuple,
)

# Third party libraries
from aioextensions import (
    resolve,
    in_process,
)

# Local libraries
from state.cache import (
    cache_decorator,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.model import (
    FindingEnum,
    SkimsVulnerabilityMetadata,
    Vulnerability,
    VulnerabilityKindEnum,
    VulnerabilityStateEnum,
)
from utils.string import (
    blocking_to_snippet,
)
from zone import (
    t,
)

ALLOWED: Set[Tuple[str, str]] = {
    ('gradle-wrapper', 'jar'),
}


@cache_decorator()
async def unverifiable_files(
    file_name: str,
    file_extension: str,
    path: str,
    raw_content: bytes,
) -> Tuple[Vulnerability, ...]:
    if (file_name, file_extension) in ALLOWED:
        return ()

    skims_metadata = SkimsVulnerabilityMetadata(
        description=t(
            key='src.lib_path.f117.unverifiable_files.description',
            path=path,
        ),
        snippet=blocking_to_snippet(
            column=0,
            content=await in_process(
                raw_content.decode,
                encoding='utf-8',
                errors='replace',
            ),
            line=1,
        )
    )

    return (
        Vulnerability(
            finding=FindingEnum.F117,
            kind=VulnerabilityKindEnum.LINES,
            state=VulnerabilityStateEnum.OPEN,
            what=path,
            where='1',
            skims_metadata=skims_metadata,
        ),
    )


async def analyze(
    file_name: str,
    file_extension: str,
    path: str,
    raw_content_generator: Callable[[], Awaitable[bytes]],
    store: EphemeralStore,
) -> None:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in {
        'bin',
        'class',
        'dll',
        'DS_Store',
        'exec',
        'hprof',
        'jar',
        'jasper',
        'pdb',
        'pyc',
    }:
        coroutines.append(unverifiable_files(
            file_name=file_name,
            file_extension=file_extension,
            path=path,
            raw_content=await raw_content_generator(),
        ))

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
