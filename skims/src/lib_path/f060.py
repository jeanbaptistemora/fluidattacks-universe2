# Standard library
import ast
from itertools import (
    chain,
)
from typing import (
    Awaitable,
    Callable,
    Iterator,
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
from lib_path.common import (
    EXTENSIONS_PYTHON,
)
from state import (
    cache_decorator,
)
from utils.ast import (
    iterate_nodes,
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


def _python_generic_exceptions(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    node: ast.AST
    generics: Set[str] = {'BaseException', 'Exception'}

    def are_names_generic(*nodes: ast.AST) -> bool:
        return any(
            node.id in generics for node in nodes if isinstance(node, ast.Name)
        )

    vulnerable_nodes: Iterator[ast.ExceptHandler] = iterate_nodes(
        content=content,
        filters=(
            lambda node: isinstance(node, ast.ExceptHandler),
            lambda node: any((
                node.type is None,
                (isinstance(node.type, ast.Name)
                    and are_names_generic(node.type)),
                (isinstance(node.type, ast.Tuple)
                    and are_names_generic(*node.type.elts)),
            )),
        ),
    )

    return tuple(
        Vulnerability(
            finding=FindingEnum.F060,
            kind=VulnerabilityKindEnum.LINES,
            state=VulnerabilityStateEnum.OPEN,
            what=path,
            where=f'{node.lineno}',
            skims_metadata=SkimsVulnerabilityMetadata(
                description=t(
                    key='src.lib_path.f060.generic_exceptions.description',
                    lang='Python',
                    path=path,
                ),
                snippet=blocking_to_snippet(
                    column=node.col_offset,
                    content=content,
                    line=node.lineno,
                )
            )
        )
        for node in vulnerable_nodes
    )


@cache_decorator()
async def python_generic_exceptions(
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await unblock_cpu(
        _python_generic_exceptions,
        content=content,
        path=path,
    )


async def analyze(
    content_generator: Callable[[], Awaitable[str]],
    file_extension: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    coroutines: List[Awaitable[Tuple[Vulnerability, ...]]] = []

    if file_extension in EXTENSIONS_PYTHON:
        coroutines.append(python_generic_exceptions(
            content=await content_generator(),
            path=path,
        ))

    results: Tuple[Vulnerability, ...] = tuple(chain.from_iterable(
        await collect(coroutines)
    ))

    return results
