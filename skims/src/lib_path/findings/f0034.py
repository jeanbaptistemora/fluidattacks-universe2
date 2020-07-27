# Standard library
from itertools import (
    chain,
)
from typing import (
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
    get_file_contents,
)
from utils.model import (
    FindingEnum,
    Vulnerability,
    VulnerabilityKindEnum,
    VulnerabilityStateEnum,
)


def javascript_insecure_randoms(
    path: str,
    path_lines: Tuple[Tuple[int, str], ...],
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
        for line_number, line_content in path_lines
        if 'Math.random(' in line_content
    )

    return results


async def analyze(
    extension: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    path_content: str = await get_file_contents(path)
    path_lines: Tuple[Tuple[int, str], ...] = tuple(
        enumerate(path_content.splitlines()),
    )

    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if extension in ['js', 'jsx', 'ts', 'tsx']:
        coroutines.append(unblock(
            javascript_insecure_randoms,
            path=path,
            path_lines=path_lines,
        ))

    results: Tuple[Vulnerability, ...] = tuple(chain(*(
        await materialize(coroutines)
    )))

    return results
