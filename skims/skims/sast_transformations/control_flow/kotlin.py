from contextlib import (
    suppress,
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
    CfgArgs,
    Stack,
)
from typing import (
    Optional,
)
from utils import (
    graph as g,
)


def class_statements(args: CfgArgs, stack: Stack) -> None:
    stmt_ids = [
        node
        for node in g.adj_ast(args.graph, args.n_id)
        if args.graph.nodes[node].get("label_type")
        not in [";", "\n", "(", ")", ",", "comment"]
    ][1:-1]

    fn_stmts = tuple(
        node
        for node in stmt_ids
        if args.graph.nodes[node]["label_type"]
        in {"companion_object", "function_declaration"}
    )
    for fn_stmt in fn_stmts:
        stmt_ids.pop(stmt_ids.index(fn_stmt))
        args.graph.add_edge(args.n_id, fn_stmt, **g.ALWAYS)

    if stmt_ids:
        # Link to the first statement in the block
        args.graph.add_edge(args.n_id, stmt_ids[0], **g.ALWAYS)

        # Walk pairs of elements
        for stmt_a_id, stmt_b_id in pairwise(stmt_ids):
            # Mark as next_id the next statement in chain
            set_next_id(stack, stmt_b_id)
            args.generic(args.fork_n_id(stmt_a_id), stack)

        # Link recursively the last statement in the block
        with suppress(IndexError):
            propagate_next_id_from_parent(stack)
        args.generic(args.fork_n_id(stmt_ids[-1]), stack)


def loop_statement(args: CfgArgs, stack: Stack) -> None:
    if next_id := get_next_id(stack):
        args.graph.add_edge(args.n_id, next_id, **g.FALSE)

    statements = g.get_ast_childs(args.graph, args.n_id, "statements", depth=2)
    if statements:
        args.graph.add_edge(args.n_id, statements[0], **g.TRUE)
        propagate_next_id_from_parent(stack)
        args.generic(args.fork_n_id(statements[0]), stack)


def if_statement(args: CfgArgs, stack: Stack) -> None:
    match = g.match_ast_group(
        args.graph, args.n_id, "if", "else", "control_structure_body"
    )
    if match["if"] and (if_else_blocks := match["control_structure_body"]):
        if_stmts = g.get_ast_childs(
            args.graph, if_else_blocks[0], "statements"
        )
        if if_stmts:
            args.graph.add_edge(args.n_id, if_stmts[0], **g.TRUE)
            propagate_next_id_from_parent(stack)
            args.generic(args.fork_n_id(if_stmts[0]), stack)
    if (
        match["else"]
        and (if_else_blocks := match["control_structure_body"])
        and len(if_else_blocks) == 2
    ):
        else_stmts = g.get_ast_childs(
            args.graph, if_else_blocks[1], "statements"
        )
        if else_stmts:
            args.graph.add_edge(args.n_id, else_stmts[0], **g.FALSE)
            propagate_next_id_from_parent(stack)
            args.generic(args.fork_n_id(else_stmts[0]), stack)


def try_catch_statement(args: CfgArgs, stack: Stack) -> None:
    def _set_next_id(stack: Stack, next_id: Optional[str]) -> None:
        if next_id:
            set_next_id(stack, next_id)
        else:
            propagate_next_id_from_parent(stack)

    match = g.match_ast_group(
        args.graph, args.n_id, "statements", "catch_block", "finally_block"
    )
    next_id: Optional[str] = None
    if match["finally_block"]:
        finally_actions = g.match_ast(
            args.graph, match["finally_block"][0], "statements"
        )
        if finally_block := finally_actions["statements"]:
            next_id = finally_block
            propagate_next_id_from_parent(stack)
            args.generic(args.fork_n_id(finally_block), stack)

    if match["statements"]:
        try_block_id = match["statements"][0]
        args.graph.add_edge(args.n_id, try_block_id, **g.ALWAYS)
        _set_next_id(stack, next_id)
        args.generic(args.fork_n_id(try_block_id), stack)

    if match["catch_block"]:
        for catch_id in match["catch_block"]:
            catch_actions = g.match_ast(args.graph, catch_id, "statements")
            if catch_block := catch_actions["statements"]:
                args.graph.add_edge(args.n_id, catch_block, **g.MAYBE)
                _set_next_id(stack, next_id)
                args.generic(args.fork_n_id(catch_block), stack)


def when_statement(args: CfgArgs, stack: Stack) -> None:
    match = g.match_ast_group(args.graph, args.n_id, "when_entry")
    if when_options := match["when_entry"]:
        for option in when_options:
            match = g.match_ast(args.graph, option, "control_structure_body")
            if option_body := match["control_structure_body"]:
                args.graph.add_edge(args.n_id, option, **g.MAYBE)
                option_stmts = g.adj_ast(args.graph, option_body)
                if option_stmts:
                    for step_a_id, step_b_id in pairwise(
                        (option, *option_stmts)
                    ):
                        set_next_id(stack, step_b_id)
                        args.generic(args.fork_n_id(step_a_id), stack)

                    propagate_next_id_from_parent(stack)
                    args.generic(args.fork_n_id(option_stmts[-1]), stack)
