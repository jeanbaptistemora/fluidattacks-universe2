# Standar library
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

# Third party libraries
from more_itertools import (
    mark_ends,
    pairwise,
)

# Local libraries
from model import (
    graph_model,
)
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


def _step_by_step(
    graph: graph_model.Graph,
    n_id: str,
    stack: Stack,
) -> None:
    # Statements = step1 step2 ...
    stmt_ids = g.adj_ast(graph, n_id)

    # Skip { }
    if graph.nodes[n_id]['label_type'] == 'block':
        stmt_ids = stmt_ids[1:-1]

    if not stmt_ids:
        return

    # Link to the first statement in the block
    graph.add_edge(n_id, stmt_ids[0], **ALWAYS)

    # Walk pairs of elements
    for stmt_a_id, stmt_b_id in pairwise(stmt_ids):
        # Mark as next_id the next statement in chain
        _set_next_id(stack, stmt_b_id)
        _generic(graph, stmt_a_id, stack, edge_attrs=ALWAYS)

    # Link recursively the last statement in the block
    _propagate_next_id_from_parent(stack)
    _generic(graph, stmt_ids[-1], stack, edge_attrs=ALWAYS)


def _loop_statement(
    graph: graph_model.Graph,
    n_id: str,
    stack: Stack,
) -> None:
    # If there is a next node, link it as `false`, this means
    # the predicate of the for did not hold
    if next_id := _get_next_id(stack):
        graph.add_edge(n_id, next_id, **FALSE)

    # If the predicate holds as `true` then enter into the block
    c_id = g.adj_ast(graph, n_id)[-1]
    graph.add_edge(n_id, c_id, **TRUE)

    # Recurse into the for block
    _propagate_next_id_from_parent(stack)
    _generic(graph, c_id, stack, edge_attrs=ALWAYS)


def _if_statement(
    graph: graph_model.Graph,
    n_id: str,
    stack: Stack,
) -> None:
    # if ( __0__ ) __1__ else __2__
    match = g.match_ast(
        graph, n_id,
        'if',
        '__0__',
        '__1__',
        'else',
        '__2__',
    )

    if then_id := match['__1__']:
        # Link `if` to `then` statement
        graph.add_edge(n_id, then_id, **TRUE)

        # Link whatever is inside the `then` to the next statement in chain
        _propagate_next_id_from_parent(stack)
        _generic(graph, then_id, stack, edge_attrs=ALWAYS)

    if then_id := match['__2__']:
        # Link `if` to `else` statement
        graph.add_edge(n_id, then_id, **FALSE)

        # Link whatever is inside the `then` to the next statement in chain
        _propagate_next_id_from_parent(stack)
        _generic(graph, then_id, stack, edge_attrs=ALWAYS)

    # Link whatever is inside the `then` to the next statement in chain
    elif next_id := _get_next_id(stack):
        # Link `if` to the next statement after the `if`
        graph.add_edge(n_id, next_id, **FALSE)


def _link_to_last_node(
    graph: graph_model.Graph,
    n_id: str,
    stack: Stack,
) -> None:
    # Link directly to the child statements
    c_id = g.adj_ast(graph, n_id)[-1]
    graph.add_edge(n_id, c_id, **ALWAYS)

    # Recurse
    _generic(graph, c_id, stack, edge_attrs=ALWAYS)


def _try_statement(
    graph: graph_model.Graph,
    n_id: str,
    stack: Stack,
) -> None:
    # Strain the childs over the following node types
    children_stack = []
    for c_id in g.adj_ast(graph, n_id):
        c_attrs_label_type = graph.nodes[c_id]['label_type']
        if c_attrs_label_type == 'try':
            pass
        elif c_attrs_label_type in {
            'block',
            'finally_clause',
            'resource_specification',
        }:
            children_stack.append((c_id, ALWAYS))
        elif c_attrs_label_type == 'catch_clause':
            children_stack.append((c_id, MAYBE))
        else:
            raise NotImplementedError()

    # Walk the existing blocks and link them recursively
    p_id = n_id
    for _, last, (c_id, edge_attrs) in mark_ends(children_stack):
        graph.add_edge(p_id, c_id, **edge_attrs)
        p_id = c_id

        # Link child block recursively
        _propagate_next_id_from_parent(stack)
        _generic(graph, c_id, stack, edge_attrs=edge_attrs)

        # If this is the last block and we should link to a next_id, do it
        if last:
            _propagate_next_id_from_parent(stack)
            _generic(graph, c_id, stack, edge_attrs=edge_attrs)


def _generic(
    graph: graph_model.Graph,
    n_id: str,
    stack: Stack,
    *,
    edge_attrs: EdgeAttrs,
) -> None:
    n_attrs = graph.nodes[n_id]
    n_attrs_label_type = n_attrs['label_type']

    stack.append(dict(type=n_attrs_label_type))

    for types, walker in (
        ({'block',
          'expression_statement'},
         _step_by_step),
        ({'catch_clause'},
         _link_to_last_node),
        ({'for_statement',
          'enhanced_for_statement',
          'while_statement'},
         _loop_statement),
        ({'if_statement'},
         _if_statement),
        ({'method_declaration'},
         _link_to_last_node),
        ({'try_statement',
          'try_with_resources_statement'},
         _try_statement),
    ):
        if n_attrs_label_type in types:
            walker(graph, n_id, stack)
            break
    else:
        if next_id := stack[-2].pop('next_id', None):
            if n_id != next_id:
                graph.add_edge(n_id, next_id, **edge_attrs)

    stack.pop()


def add(graph: graph_model.Graph) -> None:
    for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='method_declaration',
    )):
        _generic(graph, n_id, [], edge_attrs=ALWAYS)
