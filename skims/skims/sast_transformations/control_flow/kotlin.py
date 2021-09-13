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
    GenericType,
    get_next_id,
    link_to_last_node,
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
    Optional,
    Tuple,
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

    for walker in kotlin_walkers:
        if n_attrs_label_type in walker.applicable_node_label_types:
            walker.walk_fun(graph, n_id, stack)
            break
    else:
        if (next_id := stack[-2].pop("next_id", None)) and n_id != next_id:
            graph.add_edge(n_id, next_id, **edge_attrs)

    stack.pop()


def _class_statements(
    graph: Graph, n_id: str, stack: Stack, *, _generic: GenericType
) -> None:
    stmt_ids = [
        node
        for node in g.adj_ast(graph, n_id)
        if graph.nodes[node].get("label_type")
        not in [";", "\n", "(", ")", ",", "comment"]
    ][1:-1]

    fn_stmts = tuple(
        node
        for node in stmt_ids
        if graph.nodes[node]["label_type"]
        in {"companion_object", "function_declaration"}
    )
    for fn_stmt in fn_stmts:
        stmt_ids.pop(stmt_ids.index(fn_stmt))
        graph.add_edge(n_id, fn_stmt, **g.ALWAYS)

    if stmt_ids:
        # Link to the first statement in the block
        graph.add_edge(n_id, stmt_ids[0], **g.ALWAYS)

        # Walk pairs of elements
        for stmt_a_id, stmt_b_id in pairwise(stmt_ids):
            # Mark as next_id the next statement in chain
            set_next_id(stack, stmt_b_id)
            _generic(graph, stmt_a_id, stack, edge_attrs=g.ALWAYS)

        # Link recursively the last statement in the block
        with suppress(IndexError):
            propagate_next_id_from_parent(stack)
        _generic(graph, stmt_ids[-1], stack, edge_attrs=g.ALWAYS)


def _loop_statement(
    graph: Graph, n_id: str, stack: Stack, *, _generic: GenericType
) -> None:
    if next_id := get_next_id(stack):
        graph.add_edge(n_id, next_id, **g.FALSE)

    statements = g.get_ast_childs(graph, n_id, "statements", depth=2)
    if statements:
        graph.add_edge(n_id, statements[0], **g.TRUE)
        propagate_next_id_from_parent(stack)
        _generic(graph, statements[0], stack, edge_attrs=g.ALWAYS)


def _if_statement(
    graph: Graph, n_id: str, stack: Stack, *, _generic: GenericType
) -> None:
    match = g.match_ast_group(
        graph, n_id, "if", "else", "control_structure_body"
    )
    if match["if"] and (if_else_blocks := match["control_structure_body"]):
        if_stmts = g.get_ast_childs(graph, if_else_blocks[0], "statements")
        if if_stmts:
            graph.add_edge(n_id, if_stmts[0], **g.TRUE)
            propagate_next_id_from_parent(stack)
            _generic(graph, if_stmts[0], stack, edge_attrs=g.ALWAYS)
    if (
        match["else"]
        and (if_else_blocks := match["control_structure_body"])
        and len(if_else_blocks) == 2
    ):
        else_stmts = g.get_ast_childs(graph, if_else_blocks[1], "statements")
        if else_stmts:
            graph.add_edge(n_id, else_stmts[0], **g.FALSE)
            propagate_next_id_from_parent(stack)
            _generic(graph, else_stmts[0], stack, edge_attrs=g.ALWAYS)


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


kotlin_walkers: Tuple[Walker, ...] = (
    Walker(
        applicable_node_label_types={"class_body"},
        walk_fun=partial(_class_statements, _generic=_generic),
    ),
    Walker(
        applicable_node_label_types={"for_statement", "while_statement"},
        walk_fun=partial(_loop_statement, _generic=_generic),
    ),
    Walker(
        applicable_node_label_types={"function_body", "statements"},
        walk_fun=partial(step_by_step, _generic=_generic),
    ),
    Walker(
        applicable_node_label_types={
            "class_declaration",
            "function_declaration",
            "companion_object",
        },
        walk_fun=partial(link_to_last_node, _generic=_generic),
    ),
    Walker(
        applicable_node_label_types={"if_expression"},
        walk_fun=partial(_if_statement, _generic=_generic),
    ),
    Walker(
        applicable_node_label_types={"try_catch_expression"},
        walk_fun=partial(_try_catch_statement, _generic=_generic),
    ),
    Walker(
        applicable_node_label_types={"when_expression"},
        walk_fun=partial(_when_statement, _generic=_generic),
    ),
)


def add(graph: Graph) -> None:
    def _predicate(n_id: str) -> bool:
        return (
            g.pred_has_labels(label_type="function_declaration")(n_id)
            or g.pred_has_labels(label_type="class_declaration")(n_id)
            or g.pred_has_labels(label_type="companion_object")(n_id)
        )

    for n_id in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=_predicate,
    ):
        _generic(graph, n_id, stack=[], edge_attrs=g.ALWAYS)
