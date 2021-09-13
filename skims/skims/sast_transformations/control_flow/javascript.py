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
    Walker,
)
from typing import (
    Optional,
    Tuple,
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


def _function_declaration(
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
            graph.add_edge(pred_id, n_id, **g.ALWAYS)
            graph.add_edge(n_id, block, **g.ALWAYS)
            _generic(graph, block, stack=[], edge_attrs=g.ALWAYS)
            _next_declaration(graph, n_id, stack, edge_attrs=g.ALWAYS)


def _if_statement(
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
        graph.add_edge(n_id, then_id, **g.TRUE)

        # Link whatever is inside the `then` to the next statement in chain
        propagate_next_id_from_parent(stack)
        _generic(graph, then_id, stack, edge_attrs=g.ALWAYS)

    if else_id := match["else_clause"]:
        graph.add_edge(n_id, else_id, **g.FALSE)
        match_else = g.match_ast(graph, else_id, "else", "__0__")
        # Link `if` to `else` statement
        graph.add_edge(else_id, match_else["__0__"], **g.ALWAYS)

        # Link whatever is inside the `then` to the next statement in chain
        propagate_next_id_from_parent(stack)
        _generic(graph, match_else["__0__"], stack, edge_attrs=g.ALWAYS)

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
            graph.add_edge(n_id, next_id, **g.FALSE)


def _switch_statement(
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
        graph.add_edge(n_id, switch_case, **g.MAYBE)
        match_case = g.adj_ast(graph, switch_case)[3:]
        if not match_case:
            continue
        # Link to the first statement in the block
        graph.add_edge(switch_case, match_case[0], **g.ALWAYS)

        for stmt_a_id, stmt_b_id in pairwise(match_case):
            # Mark as next_id the next statement in chain
            set_next_id(stack, stmt_b_id)
            _generic(graph, stmt_a_id, stack, edge_attrs=g.ALWAYS)

        # Link recursively the last statement in the block
        propagate_next_id_from_parent(stack)
        _generic(graph, match_case[-1], stack, edge_attrs=g.ALWAYS)


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

    for walker in javascript_walkers:
        if n_attrs_label_type in walker.applicable_node_label_types:
            walker.walk_fun(graph, n_id, stack)
            break
    else:
        _next_declaration(graph, n_id, stack, edge_attrs=edge_attrs)

    stack.pop()


def _unnamed_function(graph: Graph, n_id: str, stack: Stack) -> None:
    current_node_adj = g.adj_cfg(graph, n_id)
    node_attrs = graph.nodes[n_id]
    if "label_field_body" not in node_attrs:
        return

    for pred_id in g.pred_ast_lazy(graph, n_id, depth=-1):
        adj_ids = g.adj_cfg(graph, pred_id)
        if not (adj_ids or g.pred_cfg(graph, pred_id)):
            continue

        last_statement: Optional[str] = None
        if len(adj_ids) == 1 and adj_ids[0] != n_id:
            last_statement = adj_ids[0]

        # remove cfg attrs
        for adj_id in adj_ids:
            g.remove_cfg(graph, pred_id, adj_id)
        for adj_id in current_node_adj:
            # remove cfg attrs
            g.remove_cfg(graph, n_id, adj_id)

        # add edge with first cfp parent
        graph.add_edge(pred_id, n_id, **g.ALWAYS)

        graph.add_edge(n_id, node_attrs["label_field_body"], **g.ALWAYS)
        _generic(
            graph,
            node_attrs["label_field_body"],
            stack=stack,
            edge_attrs=g.ALWAYS,
        )

        # get last statement in edge block statements
        function_statements = g.adj_cfg(
            graph, node_attrs["label_field_body"], depth=-1
        )
        for adj in current_node_adj:
            graph.add_edge(function_statements[-1], adj, **g.ALWAYS)
        if last_statement:
            graph.add_edge(function_statements[-1], last_statement, **g.ALWAYS)

        break


javascript_walkers: Tuple[Walker, ...] = (
    Walker(
        applicable_node_label_types={
            "statement_block",
            "expression_statement",
            "program",
        },
        walk_fun=partial(step_by_step, _generic=_generic),
    ),
    Walker(
        applicable_node_label_types={"catch_clause", "finally_clause"},
        walk_fun=partial(catch_statement, _generic=_generic),
    ),
    Walker(
        applicable_node_label_types={"if_statement"},
        walk_fun=_if_statement,
    ),
    Walker(
        applicable_node_label_types={"function_declaration"},
        walk_fun=_function_declaration,
    ),
    Walker(
        applicable_node_label_types={"switch_statement"},
        walk_fun=_switch_statement,
    ),
    Walker(
        applicable_node_label_types={"try_statement"},
        walk_fun=partial(
            try_statement,
            _generic=_generic,
            language=GraphShardMetadataLanguage.JAVASCRIPT,
        ),
    ),
    Walker(
        applicable_node_label_types={
            "for_statement",
            "do_statement",
            "while_statement",
            "for_each_statement",
            "for_in_statement",
            "for_of_statement",
        },
        walk_fun=partial(
            loop_statement,
            _generic=_generic,
            language=GraphShardMetadataLanguage.JAVASCRIPT,
        ),
    ),
)


def add(graph: Graph) -> None:
    _generic(graph, g.ROOT_NODE, stack=[], edge_attrs=g.ALWAYS)

    # some nodes must be post-processed
    for n_id, node in graph.nodes.items():
        if g.pred_has_labels(label_type="arrow_function")(
            node
        ) or g.pred_has_labels(label_type="function")(node):
            _unnamed_function(graph, n_id, [])
