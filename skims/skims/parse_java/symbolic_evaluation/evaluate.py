# Standard library
import json
from typing import (
    Tuple,
)

# Third party libraries
import networkx as nx

# Local libraries
from parse_java.symbolic_evaluation import (
    common,
)
from parse_java.symbolic_evaluation.rules import (
    generic,
)
from utils.logs import (
    blocking_log,
)


def evaluate(
    graph: nx.DiGraph,
    path: Tuple[str, ...],
) -> common.Context:
    ctx = common.ensure_context(None)

    # Walk the path and mine the nodes in order to increase the context
    for n_id in path:
        generic.evaluate(graph, n_id, ctx=ctx)

    # Remove temporal state
    ctx.pop('seen')

    # Debugging information, only visible with skims --debug
    blocking_log('debug', 'Context:\n\n%s\n', json.dumps(ctx, indent=2))

    return ctx
