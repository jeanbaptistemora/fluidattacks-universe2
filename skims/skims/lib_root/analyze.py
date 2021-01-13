# Standard library
from functools import (
    partial,
)
from typing import (
    Awaitable,
    Dict,
    Iterable,
    Set,
)

# Third party libraries
from aioextensions import (
    CPU_CORES,
    in_process,
    resolve,
)

# Local imports
from lib_path.common import (
    SHIELD,
)
from lib_root import (
    f060,
)
from parse_tree_sitter.parse import (
    get_graph_db,
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
from model import (
    core_model,
    graph_model,
)


async def analyze(
    *,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> None:
    unique_paths: Set[str] = await resolve_paths(
        exclude=CTX.config.path.exclude,
        include=CTX.config.path.include,
    )

    graph_db: graph_model.GraphDB = await get_graph_db(tuple(unique_paths))
    queries: graph_model.Queries = (
        *f060.QUERIES,
    )

    # Query the root with different methods in a CPU cluster
    vulnerabilities_lazy_iterator: Iterable[
        Awaitable[core_model.Vulnerabilities],
    ] = resolve((
        pipe(
            partial(in_process, query),
            TIMEOUT_1MIN,
            SHIELD,
        )(graph_db)
        for query in queries
    ), workers=CPU_CORES)

    for vulnerabilities_lazy in vulnerabilities_lazy_iterator:
        vulnerabilities: core_model.Vulnerabilities = (
            await vulnerabilities_lazy
        )

        for vulnerability in vulnerabilities:
            await stores[vulnerability.finding].store(vulnerability)
