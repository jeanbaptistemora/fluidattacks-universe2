# Standard library
from itertools import (
    chain,
)
from typing import (
    AsyncGenerator,
    Awaitable,
    Dict,
    List,
    Tuple,
)

# Third party libraries
from pyparsing import (
    Keyword,
    nestedExpr,
)

# Local libraries
from lib_path.grammars import (
    blocking_get_matching_lines,
    C_STYLE_COMMENT,
    DOUBLE_QUOTED_STRING,
    SINGLE_QUOTED_STRING,
)
from utils.aio import (
    materialize,
    unblock,
)
from utils.fs import (
    get_file_content,
)
from utils.model import (
    FindingEnum,
    GrammarMatch,
    SkimsVulnerabilityMetadata,
    Vulnerability,
    VulnerabilityKindEnum,
    VulnerabilityStateEnum,
)
from utils.string import (
    to_snippet,
)


def javascript_insecure_randoms(
    char_to_yx_map: Dict[int, Tuple[int, int]],
    file_content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    grammar = Keyword('Math') + '.' + Keyword('random') + nestedExpr()
    grammar.ignore(C_STYLE_COMMENT)
    grammar.ignore(SINGLE_QUOTED_STRING)
    grammar.ignore(DOUBLE_QUOTED_STRING)

    results: Tuple[Vulnerability, ...] = tuple(
        Vulnerability(
            finding=FindingEnum.F0034,
            kind=VulnerabilityKindEnum.LINES,
            state=VulnerabilityStateEnum.OPEN,
            what=path,
            where=f'{match.start_line}',
            skims_metadata=SkimsVulnerabilityMetadata(
                grammar_match=match,
                snippet=to_snippet(
                    column=match.start_column,
                    content=file_content,
                    line=match.start_line,
                )
            )
        )
        for match in blocking_get_matching_lines(
            content=file_content,
            char_to_yx_map=char_to_yx_map,
            grammar=grammar,
        )
    )

    return results


async def analyze(
    char_to_yx_map_generator: AsyncGenerator[Dict[int, Tuple[int, int]], None],
    extension: str,
    file_content_generator: AsyncGenerator[str, None],
    path: str,
) -> Tuple[Vulnerability, ...]:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if extension in ['js', 'jsx', 'ts', 'tsx']:
        coroutines.append(unblock(
            javascript_insecure_randoms,
            char_to_yx_map=await char_to_yx_map_generator.__anext__(),
            file_content=await file_content_generator.__anext__(),
            path=path,
        ))

    results: Tuple[Vulnerability, ...] = tuple(chain(*(
        await materialize(coroutines)
    )))

    return results
