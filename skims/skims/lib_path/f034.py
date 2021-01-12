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
from eval_java.evaluate import (
    traverse_vulns,
)
from lib_path.common import (
    get_vulnerabilities_from_n_attrs_iterable_blocking,
    EXTENSIONS_JAVA,
    SHIELD,
)
from graph_java.get import (
    get as java_get_graph,
)
from state.cache import (
    CACHE_1SEC,
)
from utils.function import (
    TIMEOUT_1MIN,
)
from utils.model import (
    FindingEnum,
    Grammar,
    Graph,
    Vulnerability,
)
from zone import (
    t,
)


@CACHE_1SEC
@SHIELD
@TIMEOUT_1MIN
async def java_use_of_util_random(
    graph: Graph,
    content: str,
    path: str,
) -> Tuple[Vulnerability, ...]:
    return await in_process(
        get_vulnerabilities_from_n_attrs_iterable_blocking,
        content=content,
        cwe={'330'},
        description=t(
            key='src.lib_path.f034.java_use_of_util_random.description',
            path=path,
        ),
        finding=FindingEnum.F034,
        n_attrs_iterable=traverse_vulns(
            graph=graph,
            path=path,
            input_type='insecure_random',
            sink_type='F034_INSECURE_RANDOMS',
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
