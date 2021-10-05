from contextlib import (
    suppress,
)
from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage,
)
from more_itertools import (
    pairwise,
)
from sast_transformations.control_flow.types import (
    GenericType,
    Stack,
)
from typing import (
    Dict,
    Optional,
)
from utils import (
    graph as g,
)

BLOCK_NAME: Dict[GraphShardMetadataLanguage, str] = {
    GraphShardMetadataLanguage.JAVASCRIPT: "statement_block",
    GraphShardMetadataLanguage.JAVA: "block",
    GraphShardMetadataLanguage.CSHARP: "block",
}


def get_next_id(stack: Stack) -> Optional[str]:
    # Stack[-2] is the parent level
    next_id: Optional[str] = stack[-2].get("next_id")
    return next_id


def set_next_id(stack: Stack, n_id: str) -> None:
    # Stack[-1] is the current level
    stack[-1]["next_id"] = n_id


def propagate_next_id_from_parent(
    stack: Stack,
    default_id: Optional[str] = None,
) -> None:
    # Propagate next id from parent if available
    if next_id := get_next_id(stack):
        set_next_id(stack, next_id)
    elif default_id:
        set_next_id(stack, default_id)
    else:
        stack[-1].pop("next_id", None)


def step_by_step(
    graph: Graph,
    n_id: str,
    stack: Stack,
    _generic: GenericType,
) -> None:
    # Statements = step1 step2 ...
    stmt_ids = tuple(
        node
        for node in g.adj_ast(graph, n_id)
        # skip unnecessary node
        if graph.nodes[node].get("label_type")
        not in [";", "\n", "(", ")", ",", "comment"]
    )

    # Skip { }
    if graph.nodes[n_id]["label_type"] in {
        "block",
        "function_body",
        "statement_block",
    }:
        stmt_ids = stmt_ids[1:-1]

    if not stmt_ids:
        if next_id := get_next_id(stack):
            graph.add_edge(n_id, next_id, **g.ALWAYS)
        return

    # Link to the first statement in the block
    graph.add_edge(n_id, stmt_ids[0], **g.ALWAYS)

    # Walk pairs of elements
    for stmt_a_id, stmt_b_id in pairwise(stmt_ids):
        # Mark as next_id the next statement in chain
        set_next_id(stack, stmt_b_id)
        _generic(graph, stmt_a_id, stack, edge_attrs=g.ALWAYS)

    # Put the next element after the block in the stack, if exists
    with suppress(IndexError):
        propagate_next_id_from_parent(stack)

    # Analyze last statment in the current block
    _generic(graph, stmt_ids[-1], stack, edge_attrs=g.ALWAYS)


def link_to_last_node(
    graph: Graph,
    n_id: str,
    stack: Stack,
    _generic: GenericType,
) -> None:
    # Link directly to the child statements
    c_id = g.adj_ast(graph, n_id)[-1]
    graph.add_edge(n_id, c_id, **g.ALWAYS)

    # Recurse
    _generic(graph, c_id, stack, edge_attrs=g.ALWAYS)


def if_statement(
    graph: Graph,
    n_id: str,
    stack: Stack,
    _generic: GenericType,
) -> None:
    # if ( __0__ ) __1__ else __2__
    match = g.match_ast(
        graph,
        n_id,
        "if",
        "(",
        ")",
        "__0__",
        "__1__",
        "else",
        "__2__",
    )

    if then_id := match["__1__"]:
        # Link `if` to `then` statement
        graph.add_edge(n_id, then_id, **g.TRUE)

        # Link whatever is inside the `then` to the next statement in chain
        propagate_next_id_from_parent(stack)
        _generic(graph, then_id, stack, edge_attrs=g.ALWAYS)

    if match["else"] and (else_id := match["__2__"]):
        # Link `if` to `else` statement
        graph.add_edge(n_id, else_id, **g.FALSE)

        # Link whatever is inside the `then` to the next statement in chain
        propagate_next_id_from_parent(stack)
        _generic(graph, else_id, stack, edge_attrs=g.ALWAYS)

    # Link whatever is inside the `then` to the next statement in chain
    elif (next_id := get_next_id(stack)) and next_id != n_id:
        # Link `if` to the next statement after the `if`
        for statement in g.pred_cfg_lazy(graph, n_id, depth=-1):
            if statement == next_id:
                break
        else:
            graph.add_edge(n_id, next_id, **g.FALSE)


def try_statement(
    graph: Graph,
    n_id: str,
    stack: Stack,
    _generic: GenericType,
    last_node: Optional[str] = None,
    language: Optional[GraphShardMetadataLanguage] = None,
) -> None:
    block_name = BLOCK_NAME.get(language) or "block"
    match = g.match_ast_group(
        graph, n_id, block_name, "catch_clause", "finally_clause"
    )
    # can be used by try_with_resources_statement
    last_node = last_node or n_id

    if _block_id := match[block_name]:
        block_id = _block_id.pop()
        graph.add_edge(last_node, block_id, **g.ALWAYS)
        propagate_next_id_from_parent(stack)
        _generic(graph, block_id, stack, edge_attrs=g.ALWAYS)

    if _catch_ids := match.get("catch_clause", set()):
        for catch_id in _catch_ids:
            graph.add_edge(last_node, catch_id, **g.MAYBE)
            propagate_next_id_from_parent(stack)
            _generic(graph, catch_id, stack, edge_attrs=g.ALWAYS)

    if _finally_id := match["finally_clause"]:
        finally_id = _finally_id.pop()
        graph.add_edge(last_node, finally_id, **g.ALWAYS)
        propagate_next_id_from_parent(stack)
        _generic(graph, finally_id, stack, edge_attrs=g.ALWAYS)


def catch_statement(
    graph: Graph,
    n_id: str,
    stack: Stack,
    _generic: GenericType,
) -> None:
    propagate_next_id_from_parent(stack)
    link_to_last_node(graph, n_id, stack, _generic=_generic)


def loop_statement(
    graph: Graph,
    n_id: str,
    stack: Stack,
    _generic: GenericType,
    language: Optional[GraphShardMetadataLanguage] = None,
) -> None:
    # If there is a next node, link it as `g.FALSE`, this means
    # the predicate of the for did not hold
    if (next_id := get_next_id(stack)) and graph.nodes[n_id][
        "label_type"
    ] not in {
        "do_statement",
    }:
        graph.add_edge(n_id, next_id, **g.FALSE)

    # If the predicate holds as `g.TRUE` then enter into the block
    block_name = BLOCK_NAME.get(language) or "block"
    c_id = g.adj_ast(graph, n_id, label_type=block_name)[-1]
    graph.add_edge(n_id, c_id, **g.TRUE)

    # Recurse into the for block
    propagate_next_id_from_parent(stack)
    _generic(graph, c_id, stack, edge_attrs=g.ALWAYS)
