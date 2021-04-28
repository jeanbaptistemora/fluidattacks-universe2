# Standar library
from typing import (
    Callable,
    List,
    Optional,
)

# Third party libraries
from more_itertools import (
    pairwise,
    mark_ends,
)
from mypy_extensions import NamedArg

# Local Imports
from model.graph_model import Graph
from sast_transformations import (
    ALWAYS,
    FALSE,
    MAYBE,
    TRUE,
)
from sast_transformations.control_flow.types import (
    EdgeAttrs,
    Stack,
)
from utils import (
    graph as g,
)


# Constants
GenericType = Callable[
    [
        Graph,
        str,
        List[Stack],
        NamedArg(EdgeAttrs, "edge_attrs"),  # noqa
    ],
    None,
]


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


def step_by_step(
    graph: Graph,
    n_id: str,
    stack: Stack,
    *,
    _generic: GenericType,
) -> None:
    # Statements = step1 step2 ...
    stmt_ids = tuple(
        node
        for node in g.adj_ast(graph, n_id)
        # skip unnecessary node
        if graph.nodes[node].get("label_type") != ";"
    )

    # Skip { }
    if graph.nodes[n_id]["label_type"] == "block":
        stmt_ids = stmt_ids[1:-1]

    if not stmt_ids:
        return

    # Link to the first statement in the block
    graph.add_edge(n_id, stmt_ids[0], **ALWAYS)

    # Walk pairs of elements
    for stmt_a_id, stmt_b_id in pairwise(stmt_ids):
        # Mark as next_id the next statement in chain
        set_next_id(stack, stmt_b_id)
        _generic(graph, stmt_a_id, stack, edge_attrs=ALWAYS)

    # Link recursively the last statement in the block
    propagate_next_id_from_parent(stack)
    _generic(graph, stmt_ids[-1], stack, edge_attrs=ALWAYS)


def link_to_last_node(
    graph: Graph,
    n_id: str,
    stack: Stack,
    *,
    _generic: GenericType,
) -> None:
    # Link directly to the child statements
    c_id = g.adj_ast(graph, n_id)[-1]
    graph.add_edge(n_id, c_id, **ALWAYS)

    # Recurse
    _generic(graph, c_id, stack, edge_attrs=ALWAYS)


def if_statement(
    graph: Graph,
    n_id: str,
    stack: Stack,
    *,
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
        graph.add_edge(n_id, then_id, **TRUE)

        # Link whatever is inside the `then` to the next statement in chain
        propagate_next_id_from_parent(stack)
        _generic(graph, then_id, stack, edge_attrs=ALWAYS)

    if then_id := match["__2__"]:
        # Link `if` to `else` statement
        graph.add_edge(n_id, then_id, **FALSE)

        # Link whatever is inside the `then` to the next statement in chain
        propagate_next_id_from_parent(stack)
        _generic(graph, then_id, stack, edge_attrs=ALWAYS)

    # Link whatever is inside the `then` to the next statement in chain
    elif next_id := get_next_id(stack):
        # Link `if` to the next statement after the `if`
        graph.add_edge(n_id, next_id, **FALSE)


def try_statement(
    graph: Graph,
    n_id: str,
    stack: Stack,
    *,
    _generic: GenericType,
) -> None:
    # Strain the childs over the following node types
    children_stack = []
    for c_id in g.adj_ast(graph, n_id):
        c_attrs_label_type = graph.nodes[c_id]["label_type"]
        if c_attrs_label_type in {
            "block",
            "finally_clause",
            "resource_specification",
        }:
            children_stack.append((c_id, ALWAYS))
        elif c_attrs_label_type == "catch_clause":
            children_stack.append((c_id, MAYBE))
        elif c_attrs_label_type != "try":
            raise NotImplementedError()

    # Walk the existing blocks and link them recursively
    p_id = n_id
    for _, last, (c_id, edge_attrs) in mark_ends(children_stack):
        graph.add_edge(p_id, c_id, **edge_attrs)
        p_id = c_id

        # Link child block recursively
        propagate_next_id_from_parent(stack)
        _generic(graph, c_id, stack, edge_attrs=edge_attrs)

        # If this is the last block and we should link to a next_id, do it
        if last:
            propagate_next_id_from_parent(stack)
            _generic(graph, c_id, stack, edge_attrs=edge_attrs)


def catch_statement(
    graph: Graph,
    n_id: str,
    stack: Stack,
    _generic: GenericType,
) -> None:
    propagate_next_id_from_parent(stack)
    link_to_last_node(graph, n_id, stack, _generic=_generic)
