# Standard library
from itertools import (
    chain,
)
import re
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    List,
    Tuple,
)

# Third party libraries
from aioextensions import (
    resolve,
    in_process,
)

# Local libraries
from parse_grammar import (
    parse,
)
from lib_path.common import (
    EXTENSIONS_JAVA,
    SHIELD,
)
from state.cache import (
    cache_decorator,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.graph import (
    yield_nodes,
)
from utils.model import (
    FindingEnum,
    SkimsVulnerabilityMetadata,
    Vulnerability,
    VulnerabilityKindEnum,
    VulnerabilityStateEnum,
)
from utils.string import (
    to_snippet,
)
from zone import (
    t,
)

# Constants
WS = r'\s*'
SEP = f'{WS},{WS}'


def _java_jpa_like_normal_annotation(
    model: Dict[str, Any],
) -> Tuple[Tuple[int, int], ...]:
    # Match: @Query(identifier = ..., identifier = ...)
    # Return the nodes inside. Most of the time simplified to StringLiteral
    return tuple(yield_nodes(
        value=model,
        key_predicates=(
            'NormalAnnotation'.__eq__,
        ),
        value_predicates=(
            '[0].type==`AT`',
            """
            contains(
                ['Query', 'SqlQuery'],
                [1].TypeName[0].Identifier[0].text
            )
            """,
            '[2].type==`LPAREN`',
            '[4].type==`RPAREN`',
        ),
        post_extraction=(),
        value_extraction="[3][?[0].text=='value'][2]|[0]",
    ))


def _java_jpa_like_single_element_annotation(
    model: Dict[str, Any],
) -> Tuple[Tuple[int, int], ...]:
    # Match: @Query(...)
    # Return the nodes inside. Most of the time simplified to StringLiteral
    return tuple(yield_nodes(
        value=model,
        key_predicates=(
            'SingleElementAnnotation'.__eq__,
        ),
        value_predicates=(
            '[0].type==`AT`',
            """
            contains(
                ['Query', 'SqlQuery'],
                [1].TypeName[0].Identifier[0].text
            )
            """,
            '[2].type==`LPAREN`',
            '[4].type==`RPAREN`',
        ),
        value_extraction='[3].ElementValue',
        pre_extraction=(),
    ))


def _java_jpa_like(model: Dict[str, Any]) -> Tuple[Tuple[int, int], ...]:

    def _has_like_injection(statement: str) -> bool:
        roots = (
            # like %x
            r'like\s+%{}',
            # like x%
            r'like\s+{}%',
            # like %x%
            r'like\s+%{}%',
            # like concat('%',   x)
            rf"like\s+concat\('%'{SEP}{{}}\)",
            # like concat(x,  '%')
            rf"like\s+concat\({{}}{SEP}'%'\)",
            # like concat('%',   x,'%')
            rf"like\s+concat\('%'{SEP}{{}}{SEP}'%'\)",
        )
        variables = (
            # :#{[0]}
            r':\#\{\[\d+\]\}',
            # :lastname
            r':[a-z0-9_\$]+',
            # ?0
            r'\?\d+',
        )
        statement = statement.lower()

        for var in variables:
            for root in roots:
                if re.search(root.format(var), statement):
                    return True
        return False

    def _check_like_injection(node: Any) -> Tuple[bool, int, int]:
        if isinstance(node, dict) and node['type'] == 'StringLiteral':
            return _has_like_injection(node['text']), node['l'], node['c']

        return False, 0, 0

    return tuple(
        (line_no, column_no)
        for vulnerable, line_no, column_no in map(_check_like_injection, chain(
            _java_jpa_like_normal_annotation(model),
            _java_jpa_like_single_element_annotation(model),
        ))
        if vulnerable
    )


@cache_decorator()
@SHIELD
async def java_jpa_like(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    if not content:
        return ()

    model = await parse('Java9', path)
    results = await in_process(_java_jpa_like, model)

    return tuple([
        Vulnerability(
            finding=FindingEnum.F001_JPA,
            kind=VulnerabilityKindEnum.LINES,
            state=VulnerabilityStateEnum.OPEN,
            what=path,
            where=f'{line_no}',
            skims_metadata=SkimsVulnerabilityMetadata(
                description=t(
                    key='src.lib_path.f001_jpa.java_like.description',
                    path=path,
                ),
                snippet=await to_snippet(
                    column=column,
                    content=content,
                    line=line_no,
                )
            )
        )
        for line_no, column in results
    ])


async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    store: EphemeralStore,
) -> None:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in EXTENSIONS_JAVA:
        coroutines.append(java_jpa_like(
            content=await content_generator(),
            path=path,
        ))

    for results in resolve(coroutines, worker_greediness=1):
        for result in await results:
            await store.store(result)
