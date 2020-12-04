# Standar library
from typing import (
    Any,
    Dict,
    List,
    Optional,
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
EdgeAttrs = Dict[str, str]
Frame = Any  # will add types once I discover the pattern
Stack = List[Frame]


def _get_next_id(stack: Stack) -> Optional[str]:
    # Stack[-2] is the parent level
    next_id: Optional[str] = stack[-2].get('next_id')

    return next_id


def _set_next_id(stack: Stack, n_id: str) -> None:
    # Stack[-1] is the current level
    stack[-1]['next_id'] = n_id


def _propagate_next_id_from_parent(
    stack: Stack,
    default_id: Optional[str] = None,
) -> None:
    # Propagate next id from parent if available
    if next_id := _get_next_id(stack):
        _set_next_id(stack, next_id)
    elif default_id:
        _set_next_id(stack, default_id)


def _block(
    graph: nx.DiGraph,
    n_id: str,
    stack: Stack,
) -> None:
    c_id = g.adj_ast(graph, n_id)[1]
    graph.add_edge(n_id, c_id, **ALWAYS)

    # Recurse
    _propagate_next_id_from_parent(stack)
    _generic(graph, c_id, stack, edge_attrs=ALWAYS)


def _block_statements(
    graph: nx.DiGraph,
    n_id: str,
    stack: Stack,
) -> None:
    # Statements = step1 step2 ...
    stmt_ids = g.adj_ast(graph, n_id)

    # Walk the Statements
    for first, last, (stmt_a_id, stmt_b_id) in mark_ends(pairwise(stmt_ids)):
        if first:
            # Link Block to first Statement
            graph.add_edge(n_id, stmt_a_id, **ALWAYS)

        # Mark as next_id the next statement in chain
        _set_next_id(stack, stmt_b_id)
        _generic(graph, stmt_a_id, stack, edge_attrs=ALWAYS)

        # Follow the parent next_id if exists
        if last:
            if _get_next_id(stack):
                _propagate_next_id_from_parent(stack)
            _generic(graph, stmt_b_id, stack, edge_attrs=ALWAYS)


def _expression_statements(
    graph: nx.DiGraph,
    n_id: str,
    stack: Stack,
) -> None:
    _block_statements(graph, n_id, stack)


def _for_statement(
    graph: nx.DiGraph,
    n_id: str,
    stack: Stack,
) -> None:
    # Link to the statements
    c_id = g.adj_ast(graph, n_id)[-1]
    graph.add_edge(n_id, c_id, **ALWAYS)

    # Recurse
    _propagate_next_id_from_parent(stack)
    _generic(graph, c_id, stack, edge_attrs=ALWAYS)


def _if_statement(
    graph: nx.DiGraph,
    n_id: str,
    stack: Stack,
) -> None:
    # if ( __0__ ) __1__ else __2__
    match = g.match_ast(
        graph, n_id,
        'IF',
        'LPAREN',
        '__0__',
        'RPAREN',
        '__1__',
    )

    # Link whatever is inside the `then` to the next statement in chain
    if next_id := _get_next_id(stack):
        # Link `if` to the next statement after the `if`
        graph.add_edge(n_id, next_id, **FALSE)

    if then_id := match['__1__']:
        # Link `if` to `then` statement
        graph.add_edge(n_id, then_id, **ALWAYS)

        # Link whatever is inside the `then` to the next statement in chain
        _propagate_next_id_from_parent(stack)
        _generic(graph, then_id, stack, edge_attrs=TRUE)


def _method_declaration(
    graph: nx.DiGraph,
    n_id: str,
    stack: Stack,
) -> None:
    # Link directly to the child statements
    c_id = g.adj_ast(graph, n_id)[-1]
    graph.add_edge(n_id, c_id, **ALWAYS)

    # Recurse
    _generic(graph, c_id, stack, edge_attrs=ALWAYS)


def _try_statement(
    graph: nx.DiGraph,
    n_id: str,
    stack: Stack,
) -> None:
    # Strain the childs over the following node types
    childs = g.match_ast(
        graph,
        n_id,
        # Components in order
        'TRY',
        'Block',
        'CatchClause',
        'Finally_',
    )

    # Declare blocks that actually exists
    childs_stack = [
        (c_id, edge_attrs)
        for c_id, edge_attrs in [
            (childs['Block'], ALWAYS),
            (childs['CatchClause'], MAYBE),
            (childs['Finally_'], ALWAYS),
        ]
        if c_id
    ]

    # Walk the existing blocks and link them recursively
    p_id = n_id
    for _, last, (c_id, edge_attrs) in mark_ends(childs_stack):
        graph.add_edge(p_id, c_id, **edge_attrs)
        p_id = c_id

        # Link child block recursively
        _generic(graph, c_id, stack, edge_attrs=edge_attrs)

        # If this is the last block and we should link to a next_id, do it
        if last:
            if _get_next_id(stack):
                _propagate_next_id_from_parent(stack)
            _generic(graph, c_id, stack, edge_attrs=edge_attrs)


def _generic(
    graph: nx.DiGraph,
    n_id: str,
    stack: Stack,
    *,
    edge_attrs: EdgeAttrs,
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
    elif n_attrs_label_type == 'EnhancedForStatement':
        _for_statement(graph, n_id, stack)
    elif n_attrs_label_type == 'IfThenStatement':
        _if_statement(graph, n_id, stack)
    elif n_attrs_label_type == 'MethodDeclaration':
        _method_declaration(graph, n_id, stack)
    elif n_attrs_label_type == 'TryStatement':
        _try_statement(graph, n_id, stack)
    elif next_id := stack[-2].pop('next_id', None):
        graph.add_edge(n_id, next_id, **edge_attrs)

    stack.pop()


def analyze(graph: nx.DiGraph) -> None:
    # Walk all `MethodDeclaration` nodes, for now they are our entrypoint
    # but it can be extended up-to compilation units and cross-file graphs
    for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='MethodDeclaration',
    )):
        _generic(graph, n_id, [], edge_attrs=ALWAYS)
