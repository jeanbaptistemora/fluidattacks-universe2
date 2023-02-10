from concurrent.futures import (
    Future,
    wait,
)
from concurrent.futures.process import (
    ProcessPoolExecutor,
)
from contextlib import (
    suppress,
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
    f008,
    f009,
    f011,
    f012,
    f015,
    f016,
    f017,
    f021,
    f022,
    f024,
    f031,
    f034,
    f035,
    f042,
    f052,
    f056,
    f059,
    f060,
    f063,
    f066,
    f070,
    f073,
    f083,
    f085,
    f089,
    f091,
    f096,
    f097,
    f098,
    f100,
    f107,
    f109,
    f112,
    f127,
    f128,
    f134,
    f135,
    f143,
    f148,
    f152,
    f157,
    f160,
    f164,
    f177,
    f188,
    f203,
    f211,
    f234,
    f237,
    f239,
    f246,
    f250,
    f256,
    f257,
    f258,
    f259,
    f280,
    f297,
    f300,
    f309,
    f320,
    f325,
    f333,
    f338,
    f343,
    f344,
    f350,
    f353,
    f354,
    f366,
    f368,
    f371,
    f372,
    f379,
    f381,
    f394,
    f396,
    f400,
    f401,
    f413,
    f414,
    f416,
    f423,
    f428,
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

QUERIES: graph_model.Queries = (
    *f001.QUERIES,
    *f004.QUERIES,
    *f007.QUERIES,
    *f008.QUERIES,
    *f009.QUERIES,
    *f011.QUERIES,
    *f012.QUERIES,
    *f015.QUERIES,
    *f016.QUERIES,
    *f017.QUERIES,
    *f021.QUERIES,
    *f022.QUERIES,
    *f024.QUERIES,
    *f031.QUERIES,
    *f034.QUERIES,
    *f035.QUERIES,
    *f042.QUERIES,
    *f052.QUERIES,
    *f056.QUERIES,
    *f059.QUERIES,
    *f060.QUERIES,
    *f063.QUERIES,
    *f066.QUERIES,
    *f070.QUERIES,
    *f073.QUERIES,
    *f083.QUERIES,
    *f085.QUERIES,
    *f089.QUERIES,
    *f091.QUERIES,
    *f096.QUERIES,
    *f097.QUERIES,
    *f098.QUERIES,
    *f100.QUERIES,
    *f107.QUERIES,
    *f109.QUERIES,
    *f112.QUERIES,
    *f127.QUERIES,
    *f128.QUERIES,
    *f134.QUERIES,
    *f135.QUERIES,
    *f143.QUERIES,
    *f148.QUERIES,
    *f152.QUERIES,
    *f157.QUERIES,
    *f160.QUERIES,
    *f164.QUERIES,
    *f188.QUERIES,
    *f177.QUERIES,
    *f203.QUERIES,
    *f211.QUERIES,
    *f234.QUERIES,
    *f237.QUERIES,
    *f239.QUERIES,
    *f246.QUERIES,
    *f250.QUERIES,
    *f256.QUERIES,
    *f257.QUERIES,
    *f258.QUERIES,
    *f259.QUERIES,
    *f280.QUERIES,
    *f297.QUERIES,
    *f300.QUERIES,
    *f309.QUERIES,
    *f320.QUERIES,
    *f325.QUERIES,
    *f333.QUERIES,
    *f338.QUERIES,
    *f343.QUERIES,
    *f344.QUERIES,
    *f350.QUERIES,
    *f353.QUERIES,
    *f354.QUERIES,
    *f366.QUERIES,
    *f368.QUERIES,
    *f371.QUERIES,
    *f372.QUERIES,
    *f379.QUERIES,
    *f381.QUERIES,
    *f394.QUERIES,
    *f396.QUERIES,
    *f400.QUERIES,
    *f401.QUERIES,
    *f413.QUERIES,
    *f414.QUERIES,
    *f416.QUERIES,
    *f423.QUERIES,
    *f428.QUERIES,
)


def _store_results_callback(
    stores: Dict[core_model.FindingEnum, EphemeralStore],
    future: Future,
) -> None:
    with suppress(Exception):
        results: Tuple[Vulnerability, ...] = future.result()
        for result in results:
            stores[result.finding].store(result)


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
    has_failed = False
    with ProcessPoolExecutor(
        max_workers=os.cpu_count(),
    ) as worker:
        for path in paths.ok_paths:
            _graph = get_graph_db(paths=(path,))
            futures = []
            for _, query in queries:
                future = worker.submit(query, _graph)
                future.add_done_callback(
                    partial(_store_results_callback, stores)
                )
                futures.append(future)
            _, f_failed = wait(futures, 60)
            if f_failed and not has_failed:
                has_failed = True
        if has_failed:
            for (
                process
            ) in (
                worker._processes.values()  # pylint: disable=protected-access
            ):
                process.kill()
