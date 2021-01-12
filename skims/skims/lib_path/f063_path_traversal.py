# Standard library
from typing import (
    Awaitable,
    Callable,
    List,
    Tuple,
)

# Third party libraries
from aioextensions import (
    in_process,
)

# Local libraries
from graph_java.get import (
    get as java_get_graph,
)
from lib_path.common import (
    get_vulnerabilities_from_n_attrs_iterable_blocking,
    EXTENSIONS_JAVA,
    SHIELD,
)
from eval_java.evaluate import (
    traverse_vulns,
)
from state.cache import (
    CACHE_1SEC,
)
from utils.function import (
    TIMEOUT_1MIN,
)
from utils.model import (
    Grammar,
    Graph,
    FindingEnum,
    Vulnerability,
)
from zone import (
    t,
)


@CACHE_1SEC
@SHIELD
@TIMEOUT_1MIN
async def java_path_traversal(
    graph: Graph,
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        get_vulnerabilities_from_n_attrs_iterable_blocking,
        content=content,
        cwe={'22'},
        description=t(
            key='src.lib_path.f063_path_traversal.description',
            lang='Java',
            path=path,
        ),
        finding=FindingEnum.F063_PATH_TRAVERSAL,
        n_attrs_iterable=traverse_vulns(
            graph=graph,
            path=path,
            input_type='function',
            sink_type='F063_PATH_TRAVERSAL',
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
    content: str

    if file_extension in EXTENSIONS_JAVA:
        content = await content_generator()
        graph = await java_get_graph(
            Grammar.JAVA9,
            content=content.encode(),
            path=path,
        )
        coroutines.append(java_path_traversal(
            content=content,
            graph=graph,
            path=path,
        ))

    return coroutines
