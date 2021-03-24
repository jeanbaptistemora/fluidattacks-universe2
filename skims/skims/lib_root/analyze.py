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
    f073,
)
from model import (
    core_model,
    graph_model,
)
from sast import (
    parse,
    query,
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
    pipe,
    shield,
)
from utils.logs import (
    log,
)


@shield(on_error_return=None)
async def analyze(
    *,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> None:
    unique_paths: Set[str] = await resolve_paths(
        exclude=CTX.config.path.exclude,
        include=CTX.config.path.include,
    )

    graph_db = await parse.get_graph_db(tuple(unique_paths))
    queries: graph_model.Queries = (
        *f060.QUERIES,
        *f073.QUERIES,
        *query.QUERIES,
    )
    queries_len: int = len(queries)

    # Query the root with different methods in a CPU cluster
    vulnerabilities_lazy_iterator: Iterable[
        Awaitable[core_model.Vulnerabilities],
    ] = resolve((
        pipe(
            partial(in_process, query),
            SHIELD,
        )(graph_db)
        for finding, query in queries
        if finding in CTX.config.path.lib_root.findings
    ), workers=CPU_CORES)

    for idx, vulnerabilities_lazy in enumerate(
        vulnerabilities_lazy_iterator, start=1,
    ):
        await log('info', 'Executing query %s of %s', idx, queries_len)

        vulnerabilities: core_model.Vulnerabilities = (
            await vulnerabilities_lazy
        )

        for vulnerability in vulnerabilities:
            await stores[vulnerability.finding].store(vulnerability)
