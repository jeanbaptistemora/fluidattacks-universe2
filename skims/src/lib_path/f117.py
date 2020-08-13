# Standard library
from itertools import (
    chain,
)
from typing import (
    Awaitable,
    Callable,
    List,
    Set,
    Tuple,
)

# Third party libraries
from aioextensions import (
    collect,
    unblock_cpu,
)

# Local libraries
from state.cache import (
    cache_decorator,
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
            content=await unblock_cpu(
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
) -> Tuple[Vulnerability, ...]:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in {
        'bin', 'class', 'dll', 'exec', 'hprof', 'jar', 'jasper', 'pyc',
    }:
        coroutines.append(unverifiable_files(
            file_name=file_name,
            file_extension=file_extension,
            path=path,
            raw_content=await raw_content_generator(),
        ))

    results: Tuple[Vulnerability, ...] = tuple(chain.from_iterable(
        await collect(coroutines)
    ))

    return results
