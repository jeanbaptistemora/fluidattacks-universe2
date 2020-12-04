# Standard library
from typing import (
    Awaitable,
    Callable,
    Iterator,
    List,
    Tuple,
)

# Third party libraries
from aioextensions import (
    in_process,
)
import networkx as nx

# Local libraries
from graph_java.get import (
    get as java_get_graph,
)
from lib_path.common import (
    blocking_get_vulnerabilities_from_n_attrs_iterator,
    EXTENSIONS_JAVA,
    SHIELD,
)
from eval_java.evaluate import (
    is_vulnerable,
)
from state.cache import (
    CACHE_1SEC,
)
from utils import (
    graph as g,
)
from utils.model import (
    Grammar,
    FindingEnum,
    Vulnerability,
)
from zone import (
    t,
)


def _java_path_traversal(
    content: str,
    graph: nx.DiGraph,
    path: str,
) -> Tuple[Vulnerability, ...]:
    sink_type = 'F063_PATH_TRAVERSAL'

    def iterator() -> Iterator[g.NAttrs]:
        for graph_path in g.flows(graph, sink_type=sink_type):
            if is_vulnerable(
                graph,
                graph_path,
                path,
                sink_type=sink_type,
            ):
                yield graph.nodes[graph_path[-1]]

    return blocking_get_vulnerabilities_from_n_attrs_iterator(
        content=content,
        cwe={'22'},
        description=t(
            key='src.lib_path.f063_path_traversal.description',
            lang='Java',
            path=path,
        ),
        finding=FindingEnum.F063_PATH_TRAVERSAL,
        n_attrs_iterator=iterator(),
        path=path,
    )


@CACHE_1SEC
@SHIELD
async def java_path_traversal(
    graph: nx.DiGraph,
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _java_path_traversal,
        content=content,
        graph=graph,
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
