# Standard library
from itertools import (
    chain,
)
from typing import (
    Tuple,
)

# Local libraries
from core.model import (
    FindingEnum,
    KindEnum,
    SkimResult,
)
from utils.fs import (
    file_as_lines,
)


def javascript_insecure_randoms(
    file: str,
    lines: Tuple[Tuple[int, str], ...],
) -> Tuple[SkimResult, ...]:
    # Minimalistic proof of concept so we can focus on the heavy lifting:
    #   reporting, closing, etc
    results: Tuple[SkimResult, ...] = tuple(
        SkimResult(
            finding=FindingEnum.F0034,
            what=file,
            where=f'{line_number}',
            kind=KindEnum.LINES,
        )
        for line_number, line_content in lines
        if 'Math.random(' in line_content
    )

    return results


async def run(file: str) -> Tuple[SkimResult, ...]:
    lines: Tuple[Tuple[int, str], ...] = await file_as_lines(file)

    results: Tuple[SkimResult, ...] = tuple(chain(
        javascript_insecure_randoms(file, lines),
    ))

    return results
