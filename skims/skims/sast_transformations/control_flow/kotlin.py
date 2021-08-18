from functools import (
    partial,
)
from model.graph_model import (
    Graph,
)
from sast_transformations.control_flow.common import (
    GenericType,
    link_to_last_node,
    propagate_next_id_from_parent,
    step_by_step,
)
from sast_transformations.control_flow.types import (
    EdgeAttrs,
    Stack,
)
from utils import (
    graph as g,
)


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
            {"function_body", "statements"},
            partial(step_by_step, _generic=_generic),
        ),
        (
            {"function_declaration"},
            partial(link_to_last_node, _generic=_generic),
        ),
        (
            {"try_catch_expression"},
            partial(_try_catch_statement, _generic=_generic),
        ),
    )
    for types, walker in walkers:
        if n_attrs_label_type in types:
            walker(graph, n_id, stack)
            break
    else:
        if (next_id := stack[-2].pop("next_id", None)) and n_id != next_id:
            graph.add_edge(n_id, next_id, **edge_attrs)

    stack.pop()


def _try_catch_statement(
    graph: Graph, n_id: str, stack: Stack, *, _generic: GenericType
) -> None:
    match = g.match_ast_group(graph, n_id, "statements", "catch_block")
    if match["statements"]:
        try_block_id = match["statements"][0]
        graph.add_edge(n_id, try_block_id, **g.ALWAYS)
        propagate_next_id_from_parent(stack)
        _generic(graph, try_block_id, stack, edge_attrs=g.ALWAYS)
    if match["catch_block"]:
        for catch_id in match["catch_block"]:
            catch_actions = g.match_ast(graph, catch_id, "statements")
            if catch_block := catch_actions["statements"]:
                graph.add_edge(n_id, catch_block, **g.MAYBE)
                propagate_next_id_from_parent(stack)
                _generic(graph, catch_block, stack, edge_attrs=g.ALWAYS)


def add(graph: Graph) -> None:
    for n_id in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=g.pred_has_labels(label_type="function_declaration"),
    ):
        _generic(graph, n_id, stack=[], edge_attrs=g.ALWAYS)
