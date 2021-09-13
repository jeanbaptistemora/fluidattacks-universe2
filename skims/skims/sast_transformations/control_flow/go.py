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
    if_statement,
    link_to_last_node,
    loop_statement,
    propagate_next_id_from_parent,
    set_next_id,
    step_by_step,
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


def _switch_statement(graph: Graph, n_id: str, stack: Stack) -> None:
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
                _generic(graph, step_a_id, stack, edge_attrs=g.ALWAYS)

            propagate_next_id_from_parent(stack)
            _generic(graph, case_steps[-1], stack, edge_attrs=g.ALWAYS)


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

    for walker in go_walkers:
        if n_attrs_label_type in walker.applicable_node_label_types:
            walker.walk_fun(graph, n_id, stack)
            break
    else:
        if (next_id := stack[-2].pop("next_id", None)) and n_id != next_id:
            graph.add_edge(n_id, next_id, **edge_attrs)

    stack.pop()


go_walkers: Tuple[Walker, ...] = (
    Walker(
        applicable_node_label_types={"block"},
        walk_fun=partial(step_by_step, _generic=_generic),
    ),
    Walker(
        applicable_node_label_types={
            "function_declaration",
            "method_declaration",
        },
        walk_fun=partial(link_to_last_node, _generic=_generic),
    ),
    Walker(
        applicable_node_label_types={"if_statement"},
        walk_fun=partial(if_statement, _generic=_generic),
    ),
    Walker(
        applicable_node_label_types={"for_statement"},
        walk_fun=partial(loop_statement, _generic=_generic),
    ),
    Walker(
        applicable_node_label_types={
            "expression_switch_statement",
            "type_switch_statement",
        },
        walk_fun=_switch_statement,
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
        _generic(graph, n_id, stack=[], edge_attrs=g.ALWAYS)
