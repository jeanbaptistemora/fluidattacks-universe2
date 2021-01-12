# Standard library
from typing import (
    Awaitable,
    Dict,
    Iterable,
    Set,
    Tuple,
)

# Third party libraries
from aioextensions import (
    CPU_CORES,
    in_process,
    resolve,
)
import networkx as nx

# Local imports
from lib_path.common import (
    SHIELD,
)
from parse_tree_sitter.parse import (
    get_root,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.ctx import (
    CTX,
)
from utils.fs import (
    resolve_paths,
)
from utils.function import (
    TIMEOUT_1MIN,
    pipe,
)
from utils.model import (
    FindingEnum,
    LibRootQueries,
    Vulnerability,
)


async def analyze(
    *,
    stores: Dict[FindingEnum, EphemeralStore],
) -> None:
    unique_paths: Set[str] = await resolve_paths(
        exclude=CTX.config.path.exclude,
        include=CTX.config.path.include,
    )

    root: nx.DiGraph = await get_root(tuple(unique_paths))
    queries_list: Tuple[LibRootQueries, ...] = (
    )

    # Query the root with different methods in a CPU cluster
    vulnerabilities_lazy_iterator: Iterable[
        Awaitable[Tuple[Vulnerability, ...]],
    ] = resolve((
        pipe(in_process(query, root), (
            TIMEOUT_1MIN,
            CACHE_ETERNALLY,
            SHIELD,
        ))
        for queries in queries_list
        for query in queries
    ), workers=CPU_CORES)

    for vulnerabilities_lazy in vulnerabilities_lazy_iterator:
        vulnerabilities: Tuple[Vulnerability, ...] = await vulnerabilities_lazy

        for vulnerability in vulnerabilities:
            await stores[vulnerability.finding].store(vulnerability)
