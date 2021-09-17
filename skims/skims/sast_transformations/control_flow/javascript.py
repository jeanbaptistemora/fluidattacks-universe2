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
    EdgeAttrs,
    GenericType,
    Stack,
)
from typing import (
    Optional,
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


def function_declaration(
    graph: Graph,
    n_id: str,
    stack: Stack,
    javascript_generic: GenericType,
) -> None:
    match = g.match_ast(
        graph,
        n_id,
        "statement_block",
    )
    if block := match.get("statement_block"):
        for pred_id in g.pred_cfg(graph, n_id):
            graph.add_edge(pred_id, n_id, **g.ALWAYS)
            graph.add_edge(n_id, block, **g.ALWAYS)
            javascript_generic(graph, block, [], edge_attrs=g.ALWAYS)
            _next_declaration(graph, n_id, stack, edge_attrs=g.ALWAYS)


def if_statement(
    graph: Graph,
    n_id: str,
    stack: Stack,
    javascript_generic: GenericType,
) -> None:
    # if ( __0__ ) __1__ else
    match = g.match_ast(
        graph,
        n_id,
        "if",
        "(",
        ")",
        "__0__",
        "__1__",
        "else_clause",
    )

    if then_id := match["__1__"]:
        # Link `if` to `then` statement
        graph.add_edge(n_id, then_id, **g.TRUE)

        # Link whatever is inside the `then` to the next statement in chain
        propagate_next_id_from_parent(stack)
        javascript_generic(graph, then_id, stack, edge_attrs=g.ALWAYS)

    if else_id := match["else_clause"]:
        graph.add_edge(n_id, else_id, **g.FALSE)
        match_else = g.match_ast(graph, else_id, "else", "__0__")
        # Link `if` to `else` statement
        other_id = match_else["__0__"]
        graph.add_edge(else_id, other_id, **g.ALWAYS)

        # Link whatever is inside the `then` to the next statement in chain
        propagate_next_id_from_parent(stack)
        javascript_generic(graph, other_id, stack, edge_attrs=g.ALWAYS)

    # Link whatever is inside the `then` to the next statement in chain
    elif (
        next_id := get_next_id(stack)
        # pylint:disable=used-before-assignment
    ) and next_id != n_id:
        # Link `if` to the next statement after the `if`
        for statement in g.pred_cfg_lazy(graph, n_id, depth=-1):
            if statement == next_id:
                break
        else:
            graph.add_edge(n_id, next_id, **g.FALSE)


def switch_statement(
    graph: Graph,
    n_id: str,
    stack: Stack,
    javascript_generic: GenericType,
) -> None:
    switch_body = g.match_ast(graph, n_id, "switch_body")["switch_body"]

    switch_cases = g.match_ast_group(
        graph,
        switch_body,
        "switch_case",
        "switch_default",
    )
    for switch_case in [
        *switch_cases["switch_case"],
        *switch_cases["switch_default"],
    ]:
        graph.add_edge(n_id, switch_case, **g.MAYBE)
        match_case = g.adj_ast(graph, switch_case)[3:]
        if not match_case:
            continue
        # Link to the first statement in the block
        graph.add_edge(switch_case, match_case[0], **g.ALWAYS)

        for stmt_a_id, stmt_b_id in pairwise(match_case):
            # Mark as next_id the next statement in chain
            set_next_id(stack, stmt_b_id)
            javascript_generic(graph, stmt_a_id, stack, edge_attrs=g.ALWAYS)

        # Link recursively the last statement in the block
        propagate_next_id_from_parent(stack)
        javascript_generic(graph, match_case[-1], stack, edge_attrs=g.ALWAYS)


def _unnamed_function(
    graph: Graph,
    n_id: str,
    stack: Stack,
    javascript_generic: GenericType,
) -> None:
    current_node_adj = g.adj_cfg(graph, n_id)
    node_attrs = graph.nodes[n_id]
    if "label_field_body" not in node_attrs:
        return

    for pred_id in g.pred_ast_lazy(graph, n_id, depth=-1):
        adj_ids = g.adj_cfg(graph, pred_id)
        if not (adj_ids or g.pred_cfg(graph, pred_id)):
            continue

        last_statement: Optional[str] = None
        if len(adj_ids) == 1 and adj_ids[0] != n_id:
            last_statement = adj_ids[0]

        # remove cfg attrs
        for adj_id in adj_ids:
            g.remove_cfg(graph, pred_id, adj_id)
        for adj_id in current_node_adj:
            # remove cfg attrs
            g.remove_cfg(graph, n_id, adj_id)

        # add edge with first cfp parent
        graph.add_edge(pred_id, n_id, **g.ALWAYS)

        graph.add_edge(n_id, node_attrs["label_field_body"], **g.ALWAYS)
        javascript_generic(
            graph,
            node_attrs["label_field_body"],
            stack,
            edge_attrs=g.ALWAYS,
        )

        # get last statement in edge block statements
        function_statements = g.adj_cfg(
            graph, node_attrs["label_field_body"], depth=-1
        )
        for adj in current_node_adj:
            graph.add_edge(function_statements[-1], adj, **g.ALWAYS)
        if last_statement:
            graph.add_edge(function_statements[-1], last_statement, **g.ALWAYS)

        break


def add(graph: Graph, javascript_generic: GenericType) -> None:
    javascript_generic(graph, g.ROOT_NODE, [], edge_attrs=g.ALWAYS)

    # some nodes must be post-processed
    for n_id, node in graph.nodes.items():
        if g.pred_has_labels(label_type="arrow_function")(
            node
        ) or g.pred_has_labels(label_type="function")(node):
            _unnamed_function(graph, n_id, [], javascript_generic)
