from contextlib import (
    suppress,
)
from model.graph_model import (
    Graph,
)
from more_itertools import (
    pairwise,
)
from sast_transformations.control_flow.common import (
    get_next_id,
    propagate_next_id_from_parent,
    set_next_id,
)
from sast_transformations.control_flow.types import (
    GenericType,
    Stack,
)
from typing import (
    Optional,
)
from utils import (
    graph as g,
)


def class_statements(
    graph: Graph,
    n_id: str,
    stack: Stack,
    kotlin_generic: GenericType,
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
            kotlin_generic(graph, stmt_a_id, stack, edge_attrs=g.ALWAYS)

        # Link recursively the last statement in the block
        with suppress(IndexError):
            propagate_next_id_from_parent(stack)
        kotlin_generic(graph, stmt_ids[-1], stack, edge_attrs=g.ALWAYS)


def loop_statement(
    graph: Graph,
    n_id: str,
    stack: Stack,
    kotlin_generic: GenericType,
) -> None:
    if next_id := get_next_id(stack):
        graph.add_edge(n_id, next_id, **g.FALSE)

    statements = g.get_ast_childs(graph, n_id, "statements", depth=2)
    if statements:
        graph.add_edge(n_id, statements[0], **g.TRUE)
        propagate_next_id_from_parent(stack)
        kotlin_generic(graph, statements[0], stack, edge_attrs=g.ALWAYS)


def if_statement(
    graph: Graph,
    n_id: str,
    stack: Stack,
    kotlin_generic: GenericType,
) -> None:
    match = g.match_ast_group(
        graph, n_id, "if", "else", "control_structure_body"
    )
    if match["if"] and (if_else_blocks := match["control_structure_body"]):
        if_stmts = g.get_ast_childs(graph, if_else_blocks[0], "statements")
        if if_stmts:
            graph.add_edge(n_id, if_stmts[0], **g.TRUE)
            propagate_next_id_from_parent(stack)
            kotlin_generic(graph, if_stmts[0], stack, edge_attrs=g.ALWAYS)
    if (
        match["else"]
        and (if_else_blocks := match["control_structure_body"])
        and len(if_else_blocks) == 2
    ):
        else_stmts = g.get_ast_childs(graph, if_else_blocks[1], "statements")
        if else_stmts:
            graph.add_edge(n_id, else_stmts[0], **g.FALSE)
            propagate_next_id_from_parent(stack)
            kotlin_generic(graph, else_stmts[0], stack, edge_attrs=g.ALWAYS)


def try_catch_statement(
    graph: Graph,
    n_id: str,
    stack: Stack,
    kotlin_generic: GenericType,
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
            kotlin_generic(graph, finally_block, stack, edge_attrs=g.ALWAYS)

    if match["statements"]:
        try_block_id = match["statements"][0]
        graph.add_edge(n_id, try_block_id, **g.ALWAYS)
        _set_next_id(stack, next_id)
        kotlin_generic(graph, try_block_id, stack, edge_attrs=g.ALWAYS)

    if match["catch_block"]:
        for catch_id in match["catch_block"]:
            catch_actions = g.match_ast(graph, catch_id, "statements")
            if catch_block := catch_actions["statements"]:
                graph.add_edge(n_id, catch_block, **g.MAYBE)
                _set_next_id(stack, next_id)
                kotlin_generic(graph, catch_block, stack, edge_attrs=g.ALWAYS)


def when_statement(
    graph: Graph,
    n_id: str,
    stack: Stack,
    kotlin_generic: GenericType,
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
                        kotlin_generic(
                            graph, step_a_id, stack, edge_attrs=g.ALWAYS
                        )

                    propagate_next_id_from_parent(stack)
                    kotlin_generic(
                        graph, option_stmts[-1], stack, edge_attrs=g.ALWAYS
                    )
