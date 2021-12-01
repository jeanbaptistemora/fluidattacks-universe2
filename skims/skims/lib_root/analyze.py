from aioextensions import (
    in_thread,
)
from lib_root import (
    f001,
    f009,
    f012,
    f017,
    f022,
    f034,
    f035,
    f042,
    f052,
    f085,
    f091,
    f096,
    f134,
    f160,
    f211,
    f237,
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
    Optional,
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
    *f001.QUERIES,
    *f009.QUERIES,
    *f012.QUERIES,
    *f017.QUERIES,
    *f022.QUERIES,
    *f034.QUERIES,
    *f035.QUERIES,
    *f042.QUERIES,
    *f052.QUERIES,
    *f085.QUERIES,
    *f091.QUERIES,
    *f096.QUERIES,
    *f134.QUERIES,
    *f160.QUERIES,
    *f211.QUERIES,
    *f237.QUERIES,
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
        if stores[finding].has_errors:
            await log(
                "warning",
                (
                    "The query %s of %s, finding %s cannot be executed,"
                    " there are some previous errors"
                ),
                idx,
                queries_len,
                finding.name,
            )
            continue

        # Ideally should be in_process but memory requirements constraint us
        # for now
        vulnerabilities: Optional[core_model.Vulnerabilities] = await shield(
            on_error_return=None
        )(in_thread)(query, graph_db)

        if vulnerabilities is None:
            await log(
                "error",
                "An error has occurred executing query %s of %s, finding %s",
                idx,
                queries_len,
                finding.name,
            )
            stores[finding]._replace(has_errors=True)
        else:
            for vulnerability in vulnerabilities:
                await stores[vulnerability.finding].store(vulnerability)
