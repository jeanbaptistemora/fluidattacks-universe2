from concurrent.futures.process import (
    ProcessPoolExecutor,
)
from contextlib import (
    ExitStack,
)
from ctx import (
    CTX,
)
from functools import (
    partial,
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
    f097,
    f098,
    f100,
    f107,
    f128,
    f131,
    f134,
    f135,
    f143,
    f148,
    f152,
    f160,
    f192,
    f211,
    f234,
    f237,
    f239,
    f280,
    f297,
    f309,
    f320,
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
)
from model import (
    core_model,
    graph_model,
)
from model.core_model import (
    Vulnerability,
)
import os
import reactivex
from reactivex import (
    operators as ops,
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
    Tuple,
)
from utils.logs import (
    log_blocking,
    log_exception_blocking,
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
    *f097.QUERIES,
    *f098.QUERIES,
    *f100.QUERIES,
    *f107.QUERIES,
    *f128.QUERIES,
    *f131.QUERIES,
    *f134.QUERIES,
    *f135.QUERIES,
    *f143.QUERIES,
    *f148.QUERIES,
    *f152.QUERIES,
    *f160.QUERIES,
    *f192.QUERIES,
    *f211.QUERIES,
    *f234.QUERIES,
    *f237.QUERIES,
    *f239.QUERIES,
    *f280.QUERIES,
    *f297.QUERIES,
    *f309.QUERIES,
    *f320.QUERIES,
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


def _handle_result(
    stores: Dict[core_model.FindingEnum, EphemeralStore],
    result: Vulnerability,
) -> None:
    stores[result.finding].store(result)


def _handle_exception(
    exception: Exception, _observable: reactivex.Observable
) -> reactivex.Observable:
    log_exception_blocking("error", exception)
    return reactivex.of(None)


def _get_graph_db(
    paths: Tuple[str, ...], total_files: int, index: int
) -> graph_model.GraphDB:
    log_blocking("info", "Processing shard %s/%s", index, total_files)
    return get_graph_db(paths)


def analyze(
    *,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
    paths: Paths,
) -> None:
    queries: graph_model.Queries = tuple(
        (finding, query)
        for finding, query in QUERIES
        if finding in CTX.config.checks
    )
    total_paths = len(paths.ok_paths)
    context_stack = ExitStack()
    context_stack_1 = ExitStack()
    executor = context_stack.enter_context(
        ProcessPoolExecutor(max_workers=os.cpu_count())
    )
    executor_1 = context_stack_1.enter_context(
        ProcessPoolExecutor(max_workers=os.cpu_count())
    )
    reactivex.from_iterable(paths.ok_paths).pipe(
        ops.map(lambda path: (path,)),  # type: ignore
        ops.flat_map_indexed(
            lambda paths, index: reactivex.from_future(  # type: ignore
                executor.submit(  # type: ignore
                    _get_graph_db,
                    paths,
                    total_paths,
                    index,
                )
            ).pipe(
                ops.catch(_handle_exception),  # type: ignore
            )
        ),
        ops.filter(lambda x: x is not None),  # type: ignore
        ops.flat_map(
            lambda graph: reactivex.from_iterable(  # type: ignore
                ((query, graph) for _, query in queries)
            )
        ),
        ops.flat_map(
            lambda item: reactivex.from_future(  # type: ignore
                executor_1.submit(item[0], None, item[1])  # type: ignore
            ).pipe(
                ops.catch(_handle_exception),  # type: ignore
            )
        ),
        ops.filter(lambda x: x is not None),  # type: ignore
        ops.flat_map(
            lambda results: reactivex.from_iterable(  # type: ignore
                result for result in results  # type: ignore
            ).pipe(ops.catch(_handle_exception))
        ),
    ).subscribe(
        on_next=partial(_handle_result, stores),
        on_error=lambda e: log_blocking("exception", e),
    )
    context_stack.close()
    context_stack_1.close()
