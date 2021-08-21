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
    GenericType,
    link_to_last_node,
    propagate_next_id_from_parent,
    set_next_id,
    step_by_step,
)
from sast_transformations.control_flow.types import (
    EdgeAttrs,
    Stack,
)
from typing import (
    Optional,
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
        (
            {"when_expression"},
            partial(_when_statement, _generic=_generic),
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
    def _set_next_id(stack: Stack, next_id: Optional[str]) -> None:
        if next_id:
            set_next_id(stack, next_id)
        else:
            propagate_next_id_from_parent(stack)

    match = g.match_ast_group(
        graph, n_id, "statements", "catch_block", "finally_block"
    )
    next_id: Optional[str] = None
    if match["finally_block"]:
        finally_actions = g.match_ast(
            graph, match["finally_block"][0], "statements"
        )
        if finally_block := finally_actions["statements"]:
            next_id = finally_block
            propagate_next_id_from_parent(stack)
            _generic(graph, finally_block, stack, edge_attrs=g.ALWAYS)

    if match["statements"]:
        try_block_id = match["statements"][0]
        graph.add_edge(n_id, try_block_id, **g.ALWAYS)
        _set_next_id(stack, next_id)
        _generic(graph, try_block_id, stack, edge_attrs=g.ALWAYS)

    if match["catch_block"]:
        for catch_id in match["catch_block"]:
            catch_actions = g.match_ast(graph, catch_id, "statements")
            if catch_block := catch_actions["statements"]:
                graph.add_edge(n_id, catch_block, **g.MAYBE)
                _set_next_id(stack, next_id)
                _generic(graph, catch_block, stack, edge_attrs=g.ALWAYS)


def _when_statement(
    graph: Graph, n_id: str, stack: Stack, *, _generic: GenericType
) -> None:
    match = g.match_ast_group(graph, n_id, "when_entry")
    if when_options := match["when_entry"]:
        for option in when_options:
            match = g.match_ast(graph, option, "control_structure_body")
            if option_body := match["control_structure_body"]:
                graph.add_edge(n_id, option, **g.MAYBE)
                option_stmts = g.adj_ast(graph, option_body)
                if option_stmts:
                    for step_a_id, step_b_id in pairwise(
                        (option, *option_stmts)
                    ):
                        set_next_id(stack, step_b_id)
                        _generic(graph, step_a_id, stack, edge_attrs=g.ALWAYS)

                    propagate_next_id_from_parent(stack)
                    _generic(
                        graph, option_stmts[-1], stack, edge_attrs=g.ALWAYS
                    )


def add(graph: Graph) -> None:
    for n_id in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=g.pred_has_labels(label_type="function_declaration"),
    ):
        _generic(graph, n_id, stack=[], edge_attrs=g.ALWAYS)
