# Standard library
from typing import (
    Dict,
    Set,
)

# Third party libraries
from aioextensions import (
    in_thread,
)

# Local imports
from lib_path.common import (
    SHIELD,
)
from lib_root import (
    f060,
    f061,
    f073,
)
from model import (
    core_model,
    graph_model,
)
from sast import (
    parse,
    query as sast_query,
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
    shield,
)
from utils.logs import (
    log,
)

QUERIES: graph_model.Queries = (
    *f060.QUERIES,
    *f061.QUERIES,
    *f073.QUERIES,
    *sast_query.QUERIES,
)


@shield(on_error_return=None)
async def analyze(
    *,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> None:
    if not any(finding in CTX.config.checks for finding, _ in QUERIES):
        # No findings will be executed, early abort
        return

    unique_paths: Set[str] = await resolve_paths(
        exclude=CTX.config.path.exclude,
        include=CTX.config.path.include,
    )

    graph_db = await parse.get_graph_db(tuple(unique_paths))
    queries: graph_model.Queries = tuple(
        (finding, query)
        for finding, query in QUERIES
        if finding in CTX.config.checks
    )
    queries_len: int = len(queries)

    for idx, (finding, query) in enumerate(queries, start=1):
        await log(
            "info",
            "Executing query %s of %s, finding %s",
            idx,
            queries_len,
            finding.name,
        )

        # Ideally should be in_process but memory requirements constraint us
        # for now
        vulnerabilities: core_model.Vulnerabilities = await SHIELD(in_thread)(
            query, graph_db
        )

        for vulnerability in vulnerabilities:
            await stores[vulnerability.finding].store(vulnerability)
