from contextlib import (
    suppress,
)
from functools import (
    partial,
)
from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage,
)
from sast_transformations import (
    ALWAYS,
    FALSE,
    TRUE,
)
from sast_transformations.control_flow.common import (
    catch_statement,
    get_next_id,
    loop_statement,
    propagate_next_id_from_parent,
    step_by_step,
    try_statement,
)
from sast_transformations.control_flow.types import (
    EdgeAttrs,
    Stack,
)
from utils import (
    graph as g,
)


def if_statement(
    graph: Graph,
    n_id: str,
    stack: Stack,
) -> None:
    # if ( __0__ ) __1__ else
    match = g.match_ast(
        graph,
        n_id,
        "if",
        "(",
        ")",
        "__0__",
        "__1__",
        "else_clause",
    )

    if then_id := match["__1__"]:
        # Link `if` to `then` statement
        graph.add_edge(n_id, then_id, **TRUE)

        # Link whatever is inside the `then` to the next statement in chain
        propagate_next_id_from_parent(stack)
        _generic(graph, then_id, stack, edge_attrs=ALWAYS)

    if else_id := match["else_clause"]:
        graph.add_edge(n_id, else_id, **FALSE)
        match_else = g.match_ast(graph, else_id, "else", "__0__")
        # Link `if` to `else` statement
        graph.add_edge(else_id, match_else["__0__"], **ALWAYS)

        # Link whatever is inside the `then` to the next statement in chain
        propagate_next_id_from_parent(stack)
        _generic(graph, match_else["__0__"], stack, edge_attrs=ALWAYS)

    # Link whatever is inside the `then` to the next statement in chain
    elif (
        next_id := get_next_id(stack)
        # pylint:disable=used-before-assignment
    ) and next_id != n_id:
        # Link `if` to the next statement after the `if`
        for statement in g.pred_cfg_lazy(graph, n_id, depth=-1):
            if statement == next_id:
                break
        else:
            graph.add_edge(n_id, next_id, **FALSE)


def _generic(
    graph: Graph,
    n_id: str,
    stack: Stack,
    *,
    edge_attrs: EdgeAttrs,
) -> None:
    n_attrs = graph.nodes[n_id]
    n_attrs_label_type = n_attrs["label_type"]

    stack.append(dict(type=n_attrs_label_type))
    walkers = (
        (
            {
                "statement_block",
                "expression_statement",
                "program",
            },
            partial(step_by_step, _generic=_generic),
        ),
        (
            {"catch_clause", "finally_clause"},
            partial(catch_statement, _generic=_generic),
        ),
        (
            {
                "if_statement",
            },
            partial(
                if_statement,
                _generic=_generic,
                language=GraphShardMetadataLanguage.JAVASCRIPT,
            ),
        ),
        (
            {
                "try_statement",
            },
            partial(
                try_statement,
                _generic=_generic,
                language=GraphShardMetadataLanguage.JAVASCRIPT,
            ),
        ),
        (
            {
                "for_statement",
                "do_statement",
                "while_statement",
                "for_each_statement",
                "for_in_statement",
                "for_of_statement",
            },
            partial(
                loop_statement,
                _generic=_generic,
                language=GraphShardMetadataLanguage.JAVASCRIPT,
            ),
        ),
    )
    for types, walker in walkers:
        if n_attrs_label_type in types:
            walker(graph, n_id, stack)
            break
    else:
        with suppress(IndexError):
            if (
                (next_id := stack[-2].pop("next_id", None))
                and n_id != next_id
                and n_id not in g.adj_cfg(graph, next_id)
            ):
                for statement in g.pred_cfg_lazy(graph, n_id, depth=-1):
                    if statement == next_id:
                        break
                else:
                    graph.add_edge(n_id, next_id, **edge_attrs)

    stack.pop()


def add(graph: Graph) -> None:
    _generic(graph, g.ROOT_NODE, stack=[], edge_attrs=ALWAYS)
