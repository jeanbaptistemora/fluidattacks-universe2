# Standar library
from typing import (
    Callable,
    List,
    Optional,
)

# Third party libraries
from more_itertools import (
    pairwise,
)
from mypy_extensions import NamedArg

# Local Imports
from model.graph_model import Graph
from sast_transformations import (
    ALWAYS,
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
    _generic: GenericType,
) -> None:
    # Link directly to the child statements
    c_id = g.adj_ast(graph, n_id)[-1]
    graph.add_edge(n_id, c_id, **ALWAYS)

    # Recurse
    _generic(graph, c_id, stack, edge_attrs=ALWAYS)
