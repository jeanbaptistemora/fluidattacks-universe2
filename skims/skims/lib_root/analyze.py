from aioextensions import (
    in_thread,
)
from lib_path.common import (
    SHIELD,
)
from lib_root import (
    f001_jpa,
    f009,
    f014,
    f017,
    f022,
    f035,
    f042,
    f052,
    f060,
    f061,
    f070_wildcard_import,
    f073,
    f074,
    f085,
    f160,
    f211,
    f234,
    f320,
    f338,
    f366,
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
from typing import (
    Dict,
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
    *f001_jpa.QUERIES,
    *f009.QUERIES,
    *f014.QUERIES,
    *f017.QUERIES,
    *f022.QUERIES,
    *f035.QUERIES,
    *f042.QUERIES,
    *f052.QUERIES,
    *f060.QUERIES,
    *f061.QUERIES,
    *f070_wildcard_import.QUERIES,
    *f073.QUERIES,
    *f074.QUERIES,
    *f085.QUERIES,
    *f160.QUERIES,
    *f211.QUERIES,
    *f234.QUERIES,
    *f320.QUERIES,
    *f338.QUERIES,
    *f366.QUERIES,
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

    unique_paths, _, _ = await resolve_paths(
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
