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
from more_itertools import (
    pairwise,
)
from sast_transformations import (
    ALWAYS,
    FALSE,
    MAYBE,
    TRUE,
)
from sast_transformations.control_flow.common import (
    catch_statement,
    get_next_id,
    loop_statement,
    propagate_next_id_from_parent,
    set_next_id,
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


def _next_declaration(
    graph: Graph,
    n_id: str,
    stack: Stack,
    *,
    edge_attrs: EdgeAttrs,
) -> None:
    with suppress(IndexError):
        if (
            (next_id := stack[-2].pop("next_id", None))
            # pylint: disable=used-before-assignment
            and n_id != next_id
            and n_id not in g.adj_cfg(graph, next_id)
        ):
            for statement in g.pred_cfg_lazy(graph, n_id, depth=-1):
                if statement == next_id:
                    break
            else:
                graph.add_edge(n_id, next_id, **edge_attrs)


def function_declaration(
    graph: Graph,
    n_id: str,
    stack: Stack,
) -> None:
    match = g.match_ast(
        graph,
        n_id,
        "statement_block",
    )
    if block := match.get("statement_block"):
        for pred_id in g.pred_cfg(graph, n_id):
            graph.add_edge(pred_id, n_id, **ALWAYS)
            graph.add_edge(n_id, block, **ALWAYS)
            _generic(graph, block, stack=[], edge_attrs=ALWAYS)
            _next_declaration(graph, n_id, stack, edge_attrs=ALWAYS)


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


def switch_statement(
    graph: Graph,
    n_id: str,
    stack: Stack,
) -> None:
    switch_body = g.match_ast(graph, n_id, "switch_body")["switch_body"]

    switch_cases = g.match_ast_group(
        graph,
        switch_body,
        "switch_case",
        "switch_default",
    )
    for switch_case in [
        *switch_cases["switch_case"],
        *switch_cases["switch_default"],
    ]:
        graph.add_edge(n_id, switch_case, **MAYBE)
        match_case = g.adj_ast(graph, switch_case)[3:]
        if not match_case:
            continue
        # Link to the first statement in the block
        graph.add_edge(switch_case, match_case[0], **ALWAYS)

        for stmt_a_id, stmt_b_id in pairwise(match_case):
            # Mark as next_id the next statement in chain
            set_next_id(stack, stmt_b_id)
            _generic(graph, stmt_a_id, stack, edge_attrs=ALWAYS)

        # Link recursively the last statement in the block
        propagate_next_id_from_parent(stack)
        _generic(graph, match_case[-1], stack, edge_attrs=ALWAYS)


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
            if_statement,
        ),
        (
            {
                "function_declaration",
            },
            function_declaration,
        ),
        (
            {
                "switch_statement",
            },
            switch_statement,
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
            walker(graph, n_id, stack)  # type: ignore
            break
    else:
        _next_declaration(graph, n_id, stack, edge_attrs=edge_attrs)

    stack.pop()


def add(graph: Graph) -> None:
    _generic(graph, g.ROOT_NODE, stack=[], edge_attrs=ALWAYS)
