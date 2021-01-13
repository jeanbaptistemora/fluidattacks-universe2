# Standard library
from typing import (
    Awaitable,
    Callable,
    List,
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
from model import (
    core_model,
    graph_model,
)
from zone import (
    t,
)


@CACHE_1SEC
@SHIELD
@TIMEOUT_1MIN
async def java_use_of_util_random(
    graph: graph_model.Graph,
    content: str,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        get_vulnerabilities_from_n_attrs_iterable_blocking,
        content=content,
        cwe={'330'},
        description=t(
            key='src.lib_path.f034.java_use_of_util_random.description',
            path=path,
        ),
        finding=core_model.FindingEnum.F034,
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
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []

    if file_extension in EXTENSIONS_JAVA:
        content = await content_generator()
        graph = await java_get_graph(
            core_model.Grammar.JAVA9,
            content=content.encode(),
            path=path,
        )
        coroutines.append(java_use_of_util_random(
            content=await content_generator(),
            graph=graph,
            path=path,
        ))

    return coroutines
