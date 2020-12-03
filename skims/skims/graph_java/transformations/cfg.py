# Standar library
from typing import (
    Any,
    List,
)

# Third party libraries
import networkx as nx
from more_itertools import (
    mark_ends,
    pairwise,
)

# Local libraries
from utils import (
    graph as g,
)

# Constants
CFG = dict(label_cfg='CFG')
ALWAYS = dict(**CFG, label_cfg_always='cfg_always')
BREAK = dict(**CFG, label_cfg_break='cfg_break')
CONTINUE = dict(**CFG, label_cfg_continue='cfg_continue')
FALSE = dict(**CFG, label_cfg_false='cfg_false')
MAYBE = dict(**CFG, label_cfg_maybe='cfg_maybe')
TRUE = dict(**CFG, label_cfg_true='cfg_true')

# Types
Frame = Any  # will add types once I discover the pattern
Stack = List[Frame]


def _block(
    graph: nx.DiGraph,
    n_id: str,
    stack: Stack,
) -> None:
    c_id = g.adj(graph, n_id)[1]
    graph.add_edge(n_id, c_id, **ALWAYS)

    # Recurse
    _generic(graph, c_id, stack=stack)


def _block_statements(
    graph: nx.DiGraph,
    n_id: str,
    stack: Stack,
) -> None:
    # Statements = step1 step2 ...
    stmt_ids = g.adj(graph, n_id)

    # Walk the Statements
    for first, last, (stmt_a_id, stmt_b_id) in mark_ends(pairwise(stmt_ids)):
        if first:
            # Link Block to first Statement
            graph.add_edge(n_id, stmt_a_id, **ALWAYS)

        if last and stack[-2].get('next_id'):
            stack[-1]['next_id'] = stack[-2]['next_id']
        else:
            stack[-1]['next_id'] = stmt_b_id

        _generic(graph, stmt_a_id, stack=stack)


def _expression_statements(
    graph: nx.DiGraph,
    n_id: str,
    stack: Stack,
) -> None:
    _block_statements(graph, n_id, stack)


def _method_declaration(
    graph: nx.DiGraph,
    n_id: str,
    stack: Stack,
) -> None:
    c_id = g.adj(graph, n_id)[-1]
    graph.add_edge(n_id, c_id, **ALWAYS)

    # Recurse
    _generic(graph, c_id, stack=stack)


def _generic(
    graph: nx.DiGraph,
    n_id: str,
    stack: Stack,
) -> None:
    n_attrs = graph.nodes[n_id]
    n_attrs_label_type = n_attrs['label_type']

    stack.append(dict(type=n_attrs_label_type))

    if n_attrs_label_type == 'Block':
        _block(graph, n_id, stack)
    elif n_attrs_label_type == 'BlockStatements':
        _block_statements(graph, n_id, stack)
    elif n_attrs_label_type == 'ExpressionStatements':
        _expression_statements(graph, n_id, stack)
    elif n_attrs_label_type == 'MethodDeclaration':
        _method_declaration(graph, n_id, stack)
    elif next_id := stack[-2].get('next_id'):
        graph.add_edge(n_id, next_id, **ALWAYS)

    stack.pop()


def analyze(graph: nx.DiGraph) -> None:
    # Walk all `MethodDeclaration` nodes, for now they are our entrypoint
    # but it can be extended up-to compilation units and cross-file graphs
    for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='MethodDeclaration',
    )):
        _generic(graph, n_id, [])
