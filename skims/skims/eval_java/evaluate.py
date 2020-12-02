# Standard library
import json
from typing import (
    Tuple,
)

# Third party libraries
import networkx as nx

# Local libraries
from eval_java.eval_rules import (
    common,
    generic as generic_eval,
    linearize,
)
from eval_java.model import (
    Statements,
)
from eval_java.taint_rules import (
    generic as generic_taint,
)
from utils.logs import (
    blocking_log,
)


def evaluate(
    graph: nx.DiGraph,
    path: Tuple[str, ...],
    *,
    allow_incomplete: bool = False,
) -> Statements:
    ctx = common.ensure_context(None)

    # Walk the path and mine the nodes in order to increase the context
    for n_id in path:
        generic_eval.evaluate(graph, n_id, ctx=ctx)

    if ctx['complete'] or allow_incomplete:
        statements = linearize.linearize(ctx['statements'])

        # Analyze how data is propagated across statements
        generic_taint.taint(statements)

        # Debugging information, only visible with skims --debug
        blocking_log('debug', '%s', json.dumps(statements, indent=2))

        return statements

    return []


def is_vulnerable(
    graph: nx.DiGraph,
    path: Tuple[str, ...],
    *,
    allow_incomplete: bool = False,
    sink_type: str,
) -> bool:
    return any(
        statement.get('sink') == sink_type
        for statement in evaluate(
            graph,
            path,
            allow_incomplete=allow_incomplete,
        )
        if statement['__danger__']
    )
