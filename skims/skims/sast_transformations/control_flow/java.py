from contextlib import (
    suppress,
)
from functools import (
    partial,
)
from model import (
    graph_model,
)
from more_itertools import (
    pairwise,
)
from sast_transformations.control_flow.common import (
    catch_statement,
    get_next_id,
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
from typing import (
    List,
    Optional,
)
from utils import (
    graph as g,
)


def _nested_method_invocation(
    graph: graph_model.Graph,
    n_id: str,
) -> List[str]:
    keys: List[str] = [n_id]
    match = g.match_ast(graph, n_id, "method_invocation")
    if next_method := match["method_invocation"]:
        keys.extend(_nested_method_invocation(graph, next_method))
    return keys


def _method_invocation(
    graph: graph_model.Graph,
    n_id: str,
    stack: Stack,
) -> None:
    nested_methods = list(reversed(_nested_method_invocation(graph, n_id)))
    for method_id in nested_methods:
        method_attrs = graph.nodes[method_id]
        for node in g.adj_ast(graph, method_attrs["label_field_arguments"])[
            1:-1
        ]:
            _generic(graph, node, stack=[], edge_attrs=g.ALWAYS)
    with suppress(IndexError):
        if next_id := get_next_id(stack):
            graph.add_edge(n_id, next_id, **g.ALWAYS)


def _lambda_expression(
    graph: graph_model.Graph,
    n_id: str,
    stack: Stack,
) -> None:
    node_attrs = graph.nodes[n_id]
    block_id = node_attrs["label_field_body"]
    graph.add_edge(n_id, block_id, **g.ALWAYS)
    _generic(graph, block_id, stack, edge_attrs=g.ALWAYS)


def _switch_expression(
    graph: graph_model.Graph,
    n_id: str,
    stack: Stack,
) -> None:
    # switch parenthesized_expression switch_block
    node_attrs = graph.nodes[n_id]
    switch_body = node_attrs["label_field_body"]
    switch_cases = g.adj_ast(graph, switch_body)[1:-1]

    groups_withot_statements = []
    for switch_group in switch_cases:
        childrens = g.adj_ast(graph, switch_group)
        graph.add_edge(n_id, switch_group, **g.MAYBE)
        statements_ids = childrens[2:]
        if not statements_ids:
            groups_withot_statements.append(switch_group)
            continue

        for _group_withot_statement in groups_withot_statements:
            graph.add_edge(
                _group_withot_statement, statements_ids[0], **g.ALWAYS
            )
        groups_withot_statements = []

        graph.add_edge(switch_group, statements_ids[0], **g.ALWAYS)

        for stmt_a_id, stmt_b_id in pairwise(statements_ids):
            # Mark as next_id the next statement in chain
            set_next_id(stack, stmt_b_id)
            _generic(graph, stmt_a_id, stack, edge_attrs=g.ALWAYS)

        # Link recursively the last statement in the block
        propagate_next_id_from_parent(stack)
        _generic(graph, statements_ids[-1], stack, edge_attrs=g.ALWAYS)


def try_with_resources_statement(
    graph: graph_model.Graph,
    n_id: str,
    stack: Stack,
) -> None:
    node_attrs = graph.nodes[n_id]
    _resources = node_attrs["label_field_resources"]

    graph.add_edge(n_id, _resources, **g.ALWAYS)
    match_resources = g.match_ast_group(graph, _resources, "resource")
    last_resource: Optional[str] = None
    for resource in match_resources.get("resource", set()):
        graph.add_edge(last_resource or _resources, resource, **g.ALWAYS)
        last_resource = resource

    try_statement(
        graph,
        n_id,
        stack,
        _generic=_generic,
        last_node=last_resource,
    )


def _generic(
    graph: graph_model.Graph,
    n_id: str,
    stack: Stack,
    *,
    edge_attrs: EdgeAttrs,
) -> None:
    n_attrs = graph.nodes[n_id]
    n_attrs_label_type = n_attrs["label_type"]

    stack.append(dict(type=n_attrs_label_type))

    if walker := WALKERS.get(n_attrs_label_type):
        walker(graph, n_id, stack)  # type: ignore
    else:
        with suppress(IndexError):
            # pylint: disable=used-before-assignment
            if (next_id := stack[-2].pop("next_id", None)) and n_id != next_id:
                graph.add_edge(n_id, next_id, **edge_attrs)

    stack.pop()


_walkers_tuple = (
    (
        {
            "block",
            "constructor_body",
            "expression_statement",
            "resource_specification",
        },
        partial(
            step_by_step,
            _generic=_generic,
        ),
    ),
    (
        {
            "catch_clause",
            "finally_clause",
        },
        partial(catch_statement, _generic=_generic),
    ),
    (
        {
            "for_statement",
            "enhanced_for_statement",
            "while_statement",
            "do_statement",
        },
        partial(loop_statement, _generic=_generic),
    ),
    (
        {
            "if_statement",
        },
        partial(if_statement, _generic=_generic),
    ),
    (
        {
            "switch_expression",
        },
        _switch_expression,
    ),
    (
        {
            "method_invocation",
        },
        _method_invocation,
    ),
    (
        {
            "lambda_expression",
        },
        _lambda_expression,
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
            "try_statement",
        },
        partial(try_statement, _generic=_generic),
    ),
    (
        {
            "try_with_resources_statement",
        },
        try_with_resources_statement,
    ),
)
WALKERS = {
    node_type: walker
    for types, walker in _walkers_tuple
    for node_type in types
}


def add(graph: graph_model.Graph) -> None:
    def _predicate(n_id: str) -> bool:
        return (
            g.pred_has_labels(
                label_type="method_declaration",
            )(n_id)
            or g.pred_has_labels(label_type="constructor_declaration")(n_id)
        )

    for n_id in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=_predicate,
    ):
        _generic(graph, n_id, stack=[], edge_attrs=g.ALWAYS)
