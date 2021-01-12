# Standard library
from typing import (
    Tuple,
)
from more_itertools import (
    pairwise,
)

# Local libraries
from eval_java.extract_rules import (
    common,
    generic as generic_extract,
    linearize,
)
from eval_java.model import (
    Statements,
)
from eval_java.eval_rules import (
    generic as generic_evaluate,
)
from utils import (
    graph as g,
)
from utils.ctx import (
    CTX,
)
from utils.encodings import (
    json_dump,
)
from utils.model import (
    Graph,
)
from utils.string import (
    get_debug_path,
)


def evaluate(
    graph: Graph,
    graph_path: Tuple[str, ...],
    path: str,
    *,
    allow_incomplete: bool = False,
    index: int,
) -> Statements:
    ctx = common.ensure_context(None)
    ctx.path_edges = dict(pairwise(graph_path))

    # Walk the path and mine the nodes in order to increase the context
    for n_id in graph_path:
        generic_extract.extract(graph, n_id, ctx=ctx)

    if CTX.debug:
        output = get_debug_path('antlr-' + path)
        with open(f'{output}.ctx.{index}.json', 'w') as handle:
            json_dump(ctx, handle, indent=2)

    if ctx.complete or allow_incomplete:
        statements = linearize.linearize(ctx.statements)

        # Analyze how data is propagated across statements
        generic_evaluate.evaluate(statements)
    else:
        statements = []

    if CTX.debug:
        output = get_debug_path('antlr-' + path)
        with open(f'{output}.stmt.{index}.json', 'w') as handle:
            json_dump(statements, handle, indent=2)

    return statements


def is_vulnerable(
    graph: Graph,
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


def traverse_vulns(
    graph: Graph,
    path: str,
    *,
    input_type: str,
    sink_type: str,
) -> Tuple[g.NAttrs, ...]:
    return tuple(
        graph.nodes[graph_path[-1]]
        for index, graph_path in g.flows(
            graph,
            input_type=input_type,
            sink_type=sink_type,
        )
        if is_vulnerable(
            graph,
            graph_path,
            path,
            sink_type=sink_type,
            index=index,
        )
    )
