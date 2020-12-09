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
from eval_java.evaluate import (
    is_vulnerable,
)
from lib_path.common import (
    blocking_get_vulnerabilities_from_n_attrs_iterator,
    EXTENSIONS_JAVA,
    SHIELD,
)
from graph_java.get import (
    get as java_get_graph,
)
from state.cache import (
    CACHE_1SEC,
)
from utils.model import (
    FindingEnum,
    Grammar,
    Vulnerability,
)
from utils import (
    graph as g,
)
from zone import (
    t,
)


def _java_use_of_util_random(
    content: str,
    graph: nx.DiGraph,
    path: str,
) -> Tuple[Vulnerability, ...]:
    sink_type = 'F034_INSECURE_RANDOMS'

    def iterator() -> Iterator[g.NAttrs]:
        for index, graph_path in g.flows(
                graph,
                sink_type=sink_type,
                input_type='insecure_random',
        ):
            if is_vulnerable(
                graph,
                graph_path,
                path,
                sink_type=sink_type,
                index=index,
            ):
                yield graph.nodes[graph_path[-1]]

    return blocking_get_vulnerabilities_from_n_attrs_iterator(
        content=content,
        cwe={'330'},
        description=t(
            key='src.lib_path.f034.java_use_of_util_random.description',
            path=path,
        ),
        finding=FindingEnum.F034,
        n_attrs_iterator=iterator(),
        path=path,
    )


@CACHE_1SEC
@SHIELD
async def java_use_of_util_random(
    graph: nx.DiGraph,
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        _java_use_of_util_random,
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

    if file_extension in EXTENSIONS_JAVA:
        content = await content_generator()
        graph = await java_get_graph(
            Grammar.JAVA9,
            content=content.encode(),
            path=path,
        )
        coroutines.append(java_use_of_util_random(
            content=await content_generator(),
            graph=graph,
            path=path,
        ))

    return coroutines
