# Standard library
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
from utils.ctx import (
    CTX,
)
from utils.encodings import (
    json_dump,
)
from utils.string import (
    get_debug_path,
)


def evaluate(
    graph: nx.DiGraph,
    graph_path: Tuple[str, ...],
    path: str,
    *,
    allow_incomplete: bool = False,
    index: int,
) -> Statements:
    ctx = common.ensure_context(None)

    # Walk the path and mine the nodes in order to increase the context
    for n_id in graph_path:
        generic_eval.evaluate(graph, n_id, ctx=ctx)

    if CTX.debug:
        with open(f'{get_debug_path(path)}.ctx.{index}.json', 'w') as handle:
            json_dump(ctx, handle, indent=2)

    if ctx.complete or allow_incomplete:
        statements = linearize.linearize(ctx.statements)

        # Analyze how data is propagated across statements
        generic_taint.taint(statements)
    else:
        statements = []

    if CTX.debug:
        with open(f'{get_debug_path(path)}.stmt.{index}.json', 'w') as handle:
            json_dump(statements, handle, indent=2)

    return statements


def is_vulnerable(
    graph: nx.DiGraph,
    graph_path: Tuple[str, ...],
    path: str,
    *,
    allow_incomplete: bool = False,
    index: int,
    sink_type: str,
) -> bool:
    return any(
        statement.meta.sink == sink_type
        for statement in evaluate(
            graph,
            graph_path,
            path,
            allow_incomplete=allow_incomplete,
            index=index,
        )
        if statement.meta.danger
    )
