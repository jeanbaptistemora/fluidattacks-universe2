# Standard library
from itertools import (
    chain,
)
from typing import (
    AsyncGenerator,
    Awaitable,
    List,
    Tuple,
)

# Local libraries
from utils.aio import (
    materialize,
    unblock,
)
from utils.fs import (
    get_file_content,
)
from utils.model import (
    FindingEnum,
    Vulnerability,
    VulnerabilityKindEnum,
    VulnerabilityStateEnum,
)


def javascript_insecure_randoms(
    file_content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    # Minimalistic proof of concept so we can focus on the heavy lifting:
    #   reporting, closing, etc
    results: Tuple[Vulnerability, ...] = tuple(
        Vulnerability(
            finding=FindingEnum.F0034,
            kind=VulnerabilityKindEnum.LINES,
            state=VulnerabilityStateEnum.OPEN,
            what=path,
            where=f'{line_number}',
        )
        for line_number, line_content in enumerate(file_content.splitlines())
        if 'Math.random(' in line_content
    )

    return results


async def analyze(
    extension: str,
    file_content_generator: AsyncGenerator[str, None],
    path: str,
) -> Tuple[Vulnerability, ...]:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if extension in ['js', 'jsx', 'ts', 'tsx']:
        coroutines.append(unblock(
            javascript_insecure_randoms,
            file_content=await file_content_generator.__anext__(),
            path=path,
        ))

    results: Tuple[Vulnerability, ...] = tuple(chain(*(
        await materialize(coroutines)
    )))

    return results
