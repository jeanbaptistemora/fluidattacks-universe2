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
    get_next_id,
    link_to_last_node as common_link_to_last_node,
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
    Optional,
    Tuple,
)
from utils import (
    graph as g,
)


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

    for walker in KOTLIN_WALKERS:
        if n_attrs_label_type in walker.applicable_node_label_types:
            walker.walk_fun(graph, n_id, stack)
            break
    else:
        # if there is no walker for the expression, stop the recursion
        # the only thing left is to check if there is a cfg statement following
        _next_declaration(graph, n_id, stack, edge_attrs=edge_attrs)

    stack.pop()


def class_statements(graph: Graph, n_id: str, stack: Stack) -> None:
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
            generic(graph, stmt_a_id, stack, edge_attrs=g.ALWAYS)

        # Link recursively the last statement in the block
        with suppress(IndexError):
            propagate_next_id_from_parent(stack)
        generic(graph, stmt_ids[-1], stack, edge_attrs=g.ALWAYS)


def loop_statement(graph: Graph, n_id: str, stack: Stack) -> None:
    if next_id := get_next_id(stack):
        graph.add_edge(n_id, next_id, **g.FALSE)

    statements = g.get_ast_childs(graph, n_id, "statements", depth=2)
    if statements:
        graph.add_edge(n_id, statements[0], **g.TRUE)
        propagate_next_id_from_parent(stack)
        generic(graph, statements[0], stack, edge_attrs=g.ALWAYS)


def if_statement(graph: Graph, n_id: str, stack: Stack) -> None:
    match = g.match_ast_group(
        graph, n_id, "if", "else", "control_structure_body"
    )
    if match["if"] and (if_else_blocks := match["control_structure_body"]):
        if_stmts = g.get_ast_childs(graph, if_else_blocks[0], "statements")
        if if_stmts:
            graph.add_edge(n_id, if_stmts[0], **g.TRUE)
            propagate_next_id_from_parent(stack)
            generic(graph, if_stmts[0], stack, edge_attrs=g.ALWAYS)
    if (
        match["else"]
        and (if_else_blocks := match["control_structure_body"])
        and len(if_else_blocks) == 2
    ):
        else_stmts = g.get_ast_childs(graph, if_else_blocks[1], "statements")
        if else_stmts:
            graph.add_edge(n_id, else_stmts[0], **g.FALSE)
            propagate_next_id_from_parent(stack)
            generic(graph, else_stmts[0], stack, edge_attrs=g.ALWAYS)


def try_catch_statement(graph: Graph, n_id: str, stack: Stack) -> None:
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
            generic(graph, finally_block, stack, edge_attrs=g.ALWAYS)

    if match["statements"]:
        try_block_id = match["statements"][0]
        graph.add_edge(n_id, try_block_id, **g.ALWAYS)
        _set_next_id(stack, next_id)
        generic(graph, try_block_id, stack, edge_attrs=g.ALWAYS)

    if match["catch_block"]:
        for catch_id in match["catch_block"]:
            catch_actions = g.match_ast(graph, catch_id, "statements")
            if catch_block := catch_actions["statements"]:
                graph.add_edge(n_id, catch_block, **g.MAYBE)
                _set_next_id(stack, next_id)
                generic(graph, catch_block, stack, edge_attrs=g.ALWAYS)


def when_statement(graph: Graph, n_id: str, stack: Stack) -> None:
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
                        generic(graph, step_a_id, stack, edge_attrs=g.ALWAYS)

                    propagate_next_id_from_parent(stack)
                    generic(
                        graph, option_stmts[-1], stack, edge_attrs=g.ALWAYS
                    )


KOTLIN_WALKERS: Tuple[Walker, ...] = (
    Walker(
        applicable_node_label_types={"class_body"},
        walk_fun=class_statements,
    ),
    Walker(
        applicable_node_label_types={"for_statement", "while_statement"},
        walk_fun=loop_statement,
    ),
    Walker(
        applicable_node_label_types={"function_body", "statements"},
        walk_fun=partial(common_step_by_step, _generic=generic),
    ),
    Walker(
        applicable_node_label_types={
            "class_declaration",
            "function_declaration",
            "companion_object",
        },
        walk_fun=partial(common_link_to_last_node, _generic=generic),
    ),
    Walker(
        applicable_node_label_types={"if_expression"},
        walk_fun=if_statement,
    ),
    Walker(
        applicable_node_label_types={"try_catch_expression"},
        walk_fun=try_catch_statement,
    ),
    Walker(
        applicable_node_label_types={"when_expression"},
        walk_fun=when_statement,
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
        generic(graph, n_id, stack=[], edge_attrs=g.ALWAYS)
