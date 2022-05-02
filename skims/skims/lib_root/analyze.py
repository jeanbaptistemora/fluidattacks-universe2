from concurrent.futures.thread import (
    ThreadPoolExecutor,
)
from contextlib import (
    suppress,
)
from ctx import (
    CTX,
)
from lib_root import (
    f001,
    f004,
    f009,
    f012,
    f016,
    f017,
    f021,
    f022,
    f034,
    f035,
    f042,
    f052,
    f066,
    f085,
    f091,
    f096,
    f134,
    f160,
    f211,
    f237,
    f239,
    f320,
    f338,
    f366,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
    graph_model,
)
from os import (
    cpu_count,
)
from sast import (
    query as sast_query,
)
from state.ephemeral import (
    EphemeralStore,
)
from typing import (
    Dict,
    Optional,
)
from utils.logs import (
    log_blocking,
)

QUERIES: graph_model.Queries = (
    *f001.QUERIES,
    *f004.QUERIES,
    *f009.QUERIES,
    *f012.QUERIES,
    *f016.QUERIES,
    *f017.QUERIES,
    *f021.QUERIES,
    *f022.QUERIES,
    *f034.QUERIES,
    *f035.QUERIES,
    *f042.QUERIES,
    *f052.QUERIES,
    *f066.QUERIES,
    *f085.QUERIES,
    *f091.QUERIES,
    *f096.QUERIES,
    *f134.QUERIES,
    *f160.QUERIES,
    *f211.QUERIES,
    *f237.QUERIES,
    *f239.QUERIES,
    *f320.QUERIES,
    *f338.QUERIES,
    *f366.QUERIES,
    *sast_query.QUERIES,
)


def analyze(
    *,
    shard_db: ShardDb,
    graph_db: graph_model.GraphDB,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> None:
    if not any(finding in CTX.config.checks for finding, _ in QUERIES):
        # No findings will be executed, early abort
        return

    queries: graph_model.Queries = tuple(
        (finding, query)
        for finding, query in QUERIES
        if finding in CTX.config.checks
    )
    queries_len: int = len(queries)

    for idx, (finding, query) in enumerate(queries, start=1):
        log_blocking(
            "info",
            "Executing query %s of %s, finding %s",
            idx,
            queries_len,
            finding.name,
        )
        if stores[finding].has_errors:
            log_blocking(
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
        vulnerabilities: Optional[core_model.Vulnerabilities] = None
        with suppress(Exception):
            vulnerabilities = query(shard_db, graph_db)

        if vulnerabilities is None:
            log_blocking(
                "error",
                "An error has occurred executing query %s of %s, finding %s",
                idx,
                queries_len,
                finding.name,
            )
            stores[finding]._replace(has_errors=True)
        else:
            with ThreadPoolExecutor(max_workers=cpu_count()) as worker:
                worker.map(
                    lambda x: stores[  # pylint: disable=unnecessary-lambda
                        x.finding
                    ].store(x),
                    vulnerabilities,
                )
