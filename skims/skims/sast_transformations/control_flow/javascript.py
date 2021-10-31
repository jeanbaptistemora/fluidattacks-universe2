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
from sast_transformations.control_flow.utils import (
    next_declaration,
)
from typing import (
    Optional,
)
from utils import (
    graph as g,
)


def function_declaration(args: CfgArgs, stack: Stack) -> None:
    match = g.match_ast(
        args.graph,
        args.n_id,
        "statement_block",
    )
    if block := match.get("statement_block"):
        for pred_id in g.pred_cfg(args.graph, args.n_id):
            args.graph.add_edge(pred_id, args.n_id, **g.ALWAYS)
            args.graph.add_edge(args.n_id, block, **g.ALWAYS)
            args.generic(args.fork_n_id(block), [])
            next_declaration(args, stack)


def if_statement(args: CfgArgs, stack: Stack) -> None:
    # if ( __0__ ) __1__ else
    match = g.match_ast(
        args.graph,
        args.n_id,
        "if",
        "(",
        ")",
        "__0__",
        "__1__",
        "else_clause",
    )

    if then_id := match["__1__"]:
        # Link `if` to `then` statement
        args.graph.add_edge(args.n_id, then_id, **g.TRUE)

        # Link whatever is inside the `then` to the next statement in chain
        propagate_next_id_from_parent(stack)
        args.generic(args.fork_n_id(then_id), stack)

    if else_id := match["else_clause"]:
        args.graph.add_edge(args.n_id, else_id, **g.FALSE)
        match_else = g.match_ast(args.graph, else_id, "else", "__0__")
        # Link `if` to `else` statement
        other_id = match_else["__0__"]
        args.graph.add_edge(else_id, other_id, **g.ALWAYS)

        # Link whatever is inside the `then` to the next statement in chain
        propagate_next_id_from_parent(stack)
        args.generic(args.fork_n_id(other_id), stack)

    # Link whatever is inside the `then` to the next statement in chain
    elif (next_id := get_next_id(stack)) and next_id != args.n_id:
        # Link `if` to the next statement after the `if`
        for statement in g.pred_cfg_lazy(args.graph, args.n_id, depth=-1):
            if statement == next_id:
                break
        else:
            args.graph.add_edge(args.n_id, next_id, **g.FALSE)


def switch_statement(args: CfgArgs, stack: Stack) -> None:
    switch_body = g.match_ast_d(args.graph, args.n_id, "switch_body")

    switch_cases = g.match_ast_group(
        args.graph,
        switch_body,
        "switch_case",
        "switch_default",
    )
    for switch_case in [
        *switch_cases["switch_case"],
        *switch_cases["switch_default"],
    ]:
        args.graph.add_edge(args.n_id, switch_case, **g.MAYBE)
        match_case = g.adj_ast(args.graph, switch_case)[3:]
        if not match_case:
            continue
        # Link to the first statement in the block
        args.graph.add_edge(switch_case, match_case[0], **g.ALWAYS)

        for stmt_a_id, stmt_b_id in pairwise(match_case):
            # Mark as next_id the next statement in chain
            set_next_id(stack, stmt_b_id)
            args.generic(args.fork_n_id(stmt_a_id), stack)

        # Link recursively the last statement in the block
        propagate_next_id_from_parent(stack)
        args.generic(args.fork_n_id(match_case[-1]), stack)


def unnamed_function(args: CfgArgs, stack: Stack) -> None:
    current_node_adj = g.adj_cfg(args.graph, args.n_id)
    node_attrs = args.graph.nodes[args.n_id]
    if "label_field_body" not in node_attrs:
        return

    for pred_id in g.pred_ast_lazy(args.graph, args.n_id, depth=-1):
        adj_ids = g.adj_cfg(args.graph, pred_id)
        if not (adj_ids or g.pred_cfg(args.graph, pred_id)):
            continue

        last_statement: Optional[str] = None
        if len(adj_ids) == 1 and adj_ids[0] != args.n_id:
            last_statement = adj_ids[0]

        # remove cfg attrs
        for adj_id in adj_ids:
            g.remove_cfg(args.graph, pred_id, adj_id)
        for adj_id in current_node_adj:
            # remove cfg attrs
            g.remove_cfg(args.graph, args.n_id, adj_id)

        # add edge with first cfp parent
        args.graph.add_edge(pred_id, args.n_id, **g.ALWAYS)

        body_id = node_attrs["label_field_body"]
        args.graph.add_edge(args.n_id, body_id, **g.ALWAYS)
        args.generic(args.fork_n_id(body_id), stack)

        # get last statement in edge block statements
        *_, last_fun_statement = g.adj_cfg(args.graph, body_id, depth=-1)
        for adj in current_node_adj:
            args.graph.add_edge(last_fun_statement, adj, **g.ALWAYS)
        if last_statement:
            args.graph.add_edge(last_fun_statement, last_statement, **g.ALWAYS)

        break
