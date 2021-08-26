from contextlib import (
    suppress,
)
from functools import (
    partial,
)
from model.graph_model import (
    Graph,
)
from more_itertools import (
    pairwise,
)
from sast_transformations.control_flow.common import (
    catch_statement,
    if_statement,
    link_to_last_node,
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


def switch_statement(
    graph: Graph,
    n_id: str,
    stack: Stack,
) -> None:
    # switch parenthesized_expression switch_block
    try:
        switch_block = g.adj_ast(graph, n_id, label_type="switch_body")[0]
    except IndexError:
        raise NotImplementedError()

    switch_sections = tuple(
        c_id
        for c_id in g.adj_ast(graph, switch_block, label_type="switch_section")
    )

    switch_flows = []
    for c_id in switch_sections:
        case_label, *cases_statements = g.adj_ast(graph, c_id)
        switch_flows.append([case_label])
        for c_c_id in cases_statements:
            switch_flows[-1].append(c_c_id)
            if graph.nodes[c_c_id]["label_type"] == "break_statement":
                break

    for stmt_ids in switch_flows:
        # Link to the first statement in the block
        graph.add_edge(n_id, stmt_ids[0], **g.MAYBE)

        # Walk pairs of elements
        for stmt_a_id, stmt_b_id in pairwise(stmt_ids):
            # Mark as next_id the next statement in chain
            set_next_id(stack, stmt_b_id)
            _generic(graph, stmt_a_id, stack, edge_attrs=g.ALWAYS)

        # Link recursively the last statement in the block
        propagate_next_id_from_parent(stack)
        _generic(graph, stmt_ids[-1], stack, edge_attrs=g.ALWAYS)


def using_statement(
    graph: Graph,
    n_id: str,
    stack: Stack,
) -> None:
    match = g.match_ast(graph, n_id, "block")
    if block_id := match["block"]:
        graph.add_edge(n_id, block_id, **g.ALWAYS)
        _generic(graph, block_id, stack, edge_attrs=g.ALWAYS)
    propagate_next_id_from_parent(stack)
    link_to_last_node(graph, n_id, stack, _generic=_generic)


def _lambda_expression(
    graph: Graph,
    n_id: str,
    stack: Stack,
) -> None:
    node_attrs = graph.nodes[n_id]
    if "label_field_body" not in node_attrs:
        return

    body_id = node_attrs["label_field_body"]
    graph.add_edge(n_id, body_id, **g.ALWAYS)
    _generic(graph, body_id, stack, edge_attrs=g.ALWAYS)


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
                "block",
                "constructor_body",
                "expression_statement",
            },
            partial(step_by_step, _generic=_generic),
        ),
        (
            {
                "constructor_declaration",
                "method_declaration",
            },
            partial(link_to_last_node, _generic=_generic),
        ),
        (
            {
                "switch_statement",
            },
            switch_statement,
        ),
        (
            {
                "using_statement",
            },
            using_statement,
        ),
        (
            {"catch_clause", "finally_clause"},
            partial(catch_statement, _generic=_generic),
        ),
        (
            {
                "if_statement",
            },
            partial(if_statement, _generic=_generic),
        ),
        (
            {
                "try_statement",
            },
            partial(try_statement, _generic=_generic),
        ),
        (
            {
                "for_statement",
                "do_statement",
                "while_statement",
                "for_each_statement",
            },
            partial(loop_statement, _generic=_generic),
        ),
        (
            {
                "lambda_expression",
            },
            _lambda_expression,
        ),
    )
    for types, walker in walkers:
        if n_attrs_label_type in types:
            walker(graph, n_id, stack)  # type: ignore
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
    def _predicate(n_attrs: str) -> bool:
        return (
            g.pred_has_labels(label_type="method_declaration")(n_attrs)
            or g.pred_has_labels(label_type="constructor_declaration")(n_attrs)
            or g.pred_has_labels(label_type="lambda_expression")(n_attrs)
        )

    for n_id in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=_predicate,
    ):
        _generic(graph, n_id, stack=[], edge_attrs=g.ALWAYS)
