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
    Iterator,
    List,
    Tuple,
)

# Third party libraries
from aioextensions import (
    in_process,
)

# Local libraries
from parse_antlr.parse import (
    parse as parse_antlr,
)
from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
    EXTENSIONS_JAVA,
    SHIELD,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from utils.function import (
    TIMEOUT_1MIN,
)
from utils.graph import (
    yield_nodes,
)
from utils.model import (
    FindingEnum,
    Grammar,
    Vulnerability,
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


def _java_jpa_like(
    content: str,
    model: Dict[str, Any],
    path: str,
) -> Tuple[Vulnerability, ...]:

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

    def iterator() -> Iterator[Tuple[int, int]]:
        for vulnerable, line_no, column_no in map(_check_like_injection, chain(
            _java_jpa_like_normal_annotation(model),
            _java_jpa_like_single_element_annotation(model),
        )):
            if vulnerable:
                yield line_no, column_no

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={'89'},
        description=t(
            key='src.lib_path.f001_jpa.java_like.description',
            path=path,
        ),
        finding=FindingEnum.F001_JPA,
        iterator=iterator(),
        path=path,
    )


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def java_jpa_like(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    if not content:
        return ()

    return await in_process(
        _java_jpa_like,
        content=content,
        model=await parse_antlr(
            Grammar.JAVA9,
            content=content.encode(),
            path=path,
        ),
        path=path,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[Tuple[Vulnerability, ...]]]:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in EXTENSIONS_JAVA:
        coroutines.append(java_jpa_like(
            content=await content_generator(),
            path=path,
        ))

    return coroutines
