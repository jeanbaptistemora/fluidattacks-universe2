# Standard library
from itertools import (
    chain,
)
from typing import (
    Tuple,
)

# Local libraries
from utils.fs import (
    file_as_lines,
)
from utils.model import (
    FindingEnum,
    Vulnerability,
    VulnerabilityKindEnum,
    VulnerabilitySourceEnum,
    VulnerabilityStateEnum,
)


def javascript_insecure_randoms(
    file: str,
    lines: Tuple[Tuple[int, str], ...],
) -> Tuple[Vulnerability, ...]:
    # Minimalistic proof of concept so we can focus on the heavy lifting:
    #   reporting, closing, etc
    results: Tuple[Vulnerability, ...] = tuple(
        Vulnerability(
            finding=FindingEnum.F0034,
            kind=VulnerabilityKindEnum.LINES,
            source=VulnerabilitySourceEnum.SKIMS,
            state=VulnerabilityStateEnum.OPEN,
            what=file,
            where=f'{line_number}',
        )
        for line_number, line_content in lines
        if 'Math.random(' in line_content
    )

    return results


async def run(file: str) -> Tuple[Vulnerability, ...]:
    lines: Tuple[Tuple[int, str], ...] = await file_as_lines(file)

    results: Tuple[Vulnerability, ...] = tuple(chain(
        javascript_insecure_randoms(file, lines),
    ))

    return results
