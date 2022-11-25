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
    f007,
    f009,
    f011,
    f012,
    f015,
    f016,
    f017,
    f021,
    f022,
    f034,
    f035,
    f042,
    f052,
    f059,
    f060,
    f063,
    f066,
    f083,
    f085,
    f091,
    f096,
    f098,
    f100,
    f107,
    f131,
    f134,
    f135,
    f143,
    f148,
    f152,
    f160,
    f211,
    f234,
    f237,
    f239,
    f280,
    f309,
    f320,
    f337,
    f338,
    f350,
    f353,
    f354,
    f366,
    f368,
    f371,
    f413,
    f414,
    f416,
    f423,
)
from lib_sast.types import (
    Paths,
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
from sast.parse import (
    get_graph_db,
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
    *f007.QUERIES,
    *f009.QUERIES,
    *f011.QUERIES,
    *f012.QUERIES,
    *f015.QUERIES,
    *f016.QUERIES,
    *f017.QUERIES,
    *f021.QUERIES,
    *f022.QUERIES,
    *f034.QUERIES,
    *f035.QUERIES,
    *f042.QUERIES,
    *f052.QUERIES,
    *f059.QUERIES,
    *f060.QUERIES,
    *f063.QUERIES,
    *f066.QUERIES,
    *f083.QUERIES,
    *f085.QUERIES,
    *f091.QUERIES,
    *f096.QUERIES,
    *f098.QUERIES,
    *f100.QUERIES,
    *f107.QUERIES,
    *f131.QUERIES,
    *f134.QUERIES,
    *f135.QUERIES,
    *f143.QUERIES,
    *f148.QUERIES,
    *f152.QUERIES,
    *f160.QUERIES,
    *f211.QUERIES,
    *f234.QUERIES,
    *f237.QUERIES,
    *f239.QUERIES,
    *f280.QUERIES,
    *f309.QUERIES,
    *f320.QUERIES,
    *f337.QUERIES,
    *f338.QUERIES,
    *f350.QUERIES,
    *f353.QUERIES,
    *f354.QUERIES,
    *f366.QUERIES,
    *f368.QUERIES,
    *f371.QUERIES,
    *f413.QUERIES,
    *f414.QUERIES,
    *f416.QUERIES,
    *f423.QUERIES,
    *sast_query.QUERIES,
)


def analyze(
    *,
    paths: Paths,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> None:
    if not any(finding in CTX.config.checks for finding, _ in QUERIES):
        # No findings will be executed, early abort
        return

    graph_db = get_graph_db(paths.ok_paths)
    shard_db = ShardDb(paths=paths)
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
