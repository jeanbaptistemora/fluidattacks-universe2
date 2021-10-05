from model.graph_model import (
    Graph,
)
from more_itertools import (
    pairwise,
)
from sast_transformations.control_flow.common import (
    link_to_last_node as common_link_to_last_node,
    propagate_next_id_from_parent,
    set_next_id,
)
from sast_transformations.control_flow.types import (
    GenericType,
    Stack,
)
from utils import (
    graph as g,
)


def switch_statement(
    graph: Graph,
    n_id: str,
    stack: Stack,
    c_sharp_generic: GenericType,
) -> None:
    # switch parenthesized_expression switch_block
    try:
        switch_block = g.adj_ast(graph, n_id, label_type="switch_body")[0]
    except IndexError as exc:
        raise NotImplementedError() from exc

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
            c_sharp_generic(graph, stmt_a_id, stack, edge_attrs=g.ALWAYS)

        # Link recursively the last statement in the block
        propagate_next_id_from_parent(stack)
        c_sharp_generic(graph, stmt_ids[-1], stack, edge_attrs=g.ALWAYS)


def using_statement(
    graph: Graph,
    n_id: str,
    stack: Stack,
    c_sharp_generic: GenericType,
) -> None:
    match = g.match_ast(graph, n_id, "block")
    if block_id := match["block"]:
        graph.add_edge(n_id, block_id, **g.ALWAYS)
        c_sharp_generic(graph, block_id, stack, edge_attrs=g.ALWAYS)
    propagate_next_id_from_parent(stack)
    common_link_to_last_node(graph, n_id, stack, _generic=c_sharp_generic)


def lambda_expression(
    graph: Graph,
    n_id: str,
    stack: Stack,
    c_sharp_generic: GenericType,
) -> None:
    node_attrs = graph.nodes[n_id]
    if "label_field_body" not in node_attrs:
        return

    body_id = node_attrs["label_field_body"]
    graph.add_edge(n_id, body_id, **g.ALWAYS)
    c_sharp_generic(graph, body_id, stack, edge_attrs=g.ALWAYS)


def add(graph: Graph, c_sharp_generic: GenericType) -> None:
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
        c_sharp_generic(graph, n_id, [], edge_attrs=g.ALWAYS)
