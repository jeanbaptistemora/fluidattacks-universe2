# Standard library
import json
from typing import (
    Tuple,
)

# Third party libraries
import networkx as nx

# Local libraries
from parse_java.assertions import (
    common,
    generic,
)
from utils.logs import (
    blocking_log,
)


def inspect(
    graph: nx.DiGraph,
    path: Tuple[str, ...],
) -> common.Context:
    ctx: common.Context = common.build_empty_context()

    # Walk the path and mine the nodes in order to increase the context
    for n_id in path:
        try:
            generic.inspect(graph, n_id, ctx=ctx)
        except NotImplementedError:
            common.warn_not_impl(inspect, path=path, n_id=n_id)
            break

    blocking_log('debug', 'Ctx: %s', json.dumps(ctx, indent=2))

    return ctx
