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
    if_statement as common_if_statement,
    link_to_last_node as common_link_to_last_node,
    loop_statement as common_loop_statement,
    propagate_next_id_from_parent,
    set_next_id,
    step_by_step as common_step_by_step,
)
from sast_transformations.control_flow.types import (
    EdgeAttrs,
    Stack,
    Walker,
)
from typing import (
    Tuple,
)
from utils import (
    graph as g,
)


def switch_statement(graph: Graph, n_id: str, stack: Stack) -> None:
    switch_flow = tuple(
        (c_id, graph.nodes[c_id]) for c_id in g.adj_ast(graph, n_id)
    )

    switch_cases_ids = []
    for (c_id, c_attrs) in switch_flow:
        if c_attrs["label_type"] in [
            "default_case",
            "expression_case",
            "type_case",
        ]:
            switch_cases_ids.append(c_id)

    for case_id in switch_cases_ids:
        graph.add_edge(n_id, case_id, **g.MAYBE)
        case_steps = tuple(
            node
            for node in g.adj_ast(graph, case_id)
            if graph.nodes[node].get("label_type") not in [":", "\n"]
        )
        # Remove the `case condition` and `default` nodes
        case_steps = (
            case_steps[2:]
            if graph.nodes[case_steps[0]]["label_type"] == "case"
            else case_steps[1:]
        )
        if case_steps:
            for step_a_id, step_b_id in pairwise((case_id, *case_steps)):
                set_next_id(stack, step_b_id)
                generic(graph, step_a_id, stack, edge_attrs=g.ALWAYS)

            propagate_next_id_from_parent(stack)
            generic(graph, case_steps[-1], stack, edge_attrs=g.ALWAYS)


def _next_declaration(
    graph: Graph,
    n_id: str,
    stack: Stack,
    *,
    edge_attrs: EdgeAttrs,
) -> None:
    with suppress(IndexError):
        # check if a following stmt is pending in parent entry of the stack
        next_id = stack[-2].pop("next_id", None)

        # if there was a following stament, it does not have the current one
        # as child and they are not the same
        if (
            next_id
            and n_id != next_id
            and n_id not in g.adj_cfg(graph, next_id)
        ):
            # check that the next node is not already part of this cfg branch
            for statement in g.pred_cfg_lazy(graph, n_id, depth=-1):
                if statement == next_id:
                    break
            else:
                # add following statement to cfg
                graph.add_edge(n_id, next_id, **edge_attrs)


def generic(
    graph: Graph,
    n_id: str,
    stack: Stack,
    *,
    edge_attrs: EdgeAttrs,
) -> None:
    n_attrs = graph.nodes[n_id]
    n_attrs_label_type = n_attrs["label_type"]

    stack.append(dict(type=n_attrs_label_type))

    for walker in GO_WALKERS:
        if n_attrs_label_type in walker.applicable_node_label_types:
            walker.walk_fun(graph, n_id, stack)
            break
    else:
        # if there is no walker for the expression, stop the recursion
        # the only thing left is to check if there is a cfg statement following
        _next_declaration(graph, n_id, stack, edge_attrs=edge_attrs)

    stack.pop()


GO_WALKERS: Tuple[Walker, ...] = (
    Walker(
        applicable_node_label_types={"block"},
        walk_fun=partial(common_step_by_step, _generic=generic),
    ),
    Walker(
        applicable_node_label_types={
            "function_declaration",
            "method_declaration",
        },
        walk_fun=partial(common_link_to_last_node, _generic=generic),
    ),
    Walker(
        applicable_node_label_types={"if_statement"},
        walk_fun=partial(common_if_statement, _generic=generic),
    ),
    Walker(
        applicable_node_label_types={"for_statement"},
        walk_fun=partial(common_loop_statement, _generic=generic),
    ),
    Walker(
        applicable_node_label_types={
            "expression_switch_statement",
            "type_switch_statement",
        },
        walk_fun=switch_statement,
    ),
)


def add(graph: Graph) -> None:
    def _predicate(n_id: str) -> bool:
        return g.pred_has_labels(label_type="function_declaration")(
            n_id
        ) or g.pred_has_labels(label_type="method_declaration")(n_id)

    for n_id in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=_predicate,
    ):
        generic(graph, n_id, stack=[], edge_attrs=g.ALWAYS)
