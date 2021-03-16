# Standard library
from itertools import (
    chain,
    product,
)
import os
from typing import (
    Any,
    Dict,
    Callable,
    cast,
    Iterable,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
)

# Third party libraries
from jmespath import (
    search as jsh,
)
import networkx as nx

# Local libraries
from model import core_model
from model.graph_model import (
    Graph,
    NAttrs,
    NAttrsPredicateFunction,
    NId,
    NIdPredicateFunction,
)
from utils.function import (
    trace,
)

from utils.system import (
    read_blocking,
)

# Constants
GRAPH_STYLE_ATTRS = {'arrowhead', 'color', 'fillcolor', 'label', 'style'}
ROOT_NODE: str = '1'


def to_svg(graph: Graph, path: str) -> bool:
    nx.drawing.nx_agraph.write_dot(graph, path)

    code, stdout, stderr = read_blocking('dot', '-O', '-T', 'svg', path)

    if code == 0:
        os.unlink(path)
        return True

    raise SystemError(f'stdout: {stdout.decode()}, stderr: {stderr.decode()}')


def has_labels(n_attrs: NAttrs, **expected_attrs: str) -> bool:
    return all(
        n_attrs.get(expected_attr) == expected_attr_value
        for expected_attr, expected_attr_value in expected_attrs.items()
    )


def pred_has_labels(**expected_attrs: str) -> NAttrsPredicateFunction:

    def predicate(n_attrs: NAttrs) -> bool:
        return has_labels(n_attrs, **expected_attrs)

    return predicate


def filter_nodes(
    graph: Graph,
    nodes: Iterable[str],
    predicate: NAttrsPredicateFunction,
) -> Tuple[str, ...]:
    result: Tuple[str, ...] = tuple(
        n_id
        for n_id in nodes
        if predicate(graph.nodes[n_id])
    )

    return result


def adj(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    _processed_n_ids: Optional[Set[str]] = None,
    **edge_attrs: str,
) -> Tuple[str, ...]:
    """Return adjacent nodes to `n_id`, following just edges with given attrs.

    - Parameter `depth` may be -1 to indicate infinite depth.
    - Search is done breadth first.
    - Nodes are returned ordered ascending by index on each level.

    This function must be used instead of graph.adj, because graph.adj
    becomes unstable (unordered) after mutating the graph, also this allow
    following just edges matching `edge_attrs`.
    """
    if depth == 0:
        return ()

    processed_n_ids: Set[str] = _processed_n_ids or set()
    if n_id in processed_n_ids:
        return ()

    processed_n_ids.add(n_id)

    results: List[str] = []

    childs: List[str] = sorted(graph.adj[n_id], key=int)

    # Append direct childs
    for c_id in childs:
        if has_labels(graph[n_id][c_id], **edge_attrs):
            results.append(c_id)

    # Recurse into childs
    if depth < 0 or depth > 1:
        for c_id in childs:
            if has_labels(graph[n_id][c_id], **edge_attrs):
                results.extend(adj(
                    graph,
                    c_id,
                    depth=depth - 1,
                    _processed_n_ids=processed_n_ids,
                    **edge_attrs,
                ))

    return tuple(results)


def adj_ast(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    **n_attrs: str,
) -> Tuple[Any, ...]:
    return tuple(
        c_id
        for c_id in adj(graph, n_id, depth, label_ast='AST')
        if has_labels(graph.nodes[c_id], **n_attrs)
    )


def adj_cfg(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    **n_attrs: str,
) -> Tuple[Any, ...]:
    return tuple(
        c_id
        for c_id in adj(graph, n_id, depth, label_cfg='CFG')
        if has_labels(graph.nodes[c_id], **n_attrs)
    )


def pred_lazy(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    **edge_attrs: str,
) -> Iterator[str]:
    """Same as `adj` but follow edges in the opposite direction."""
    if depth == 0:
        return

    p_ids: List[str] = sorted(graph.pred[n_id], key=int)

    # Append direct parents
    for p_id in p_ids:
        if has_labels(graph[p_id][n_id], **edge_attrs):
            yield p_id

    # Recurse into parents
    if depth < 0 or depth > 1:
        for p_id in p_ids:
            if has_labels(graph[p_id][n_id], **edge_attrs):
                yield from pred_lazy(
                    graph,
                    p_id,
                    depth=depth - 1,
                    **edge_attrs,
                )


def pred(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    **edge_attrs: str,
) -> Tuple[str, ...]:
    return tuple(pred_lazy(graph, n_id, depth, **edge_attrs))


def pred_ast(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    **edge_attrs: str,
) -> Tuple[str, ...]:
    return tuple(pred_ast_lazy(graph, n_id, depth, **edge_attrs))


def pred_ast_lazy(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    **edge_attrs: str,
) -> Iterator[str]:
    yield from pred_lazy(graph, n_id, depth, label_ast='AST', **edge_attrs)


def pred_cfg(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    **edge_attrs: str,
) -> Tuple[str, ...]:
    return tuple(pred_cfg_lazy(graph, n_id, depth, **edge_attrs))


def pred_cfg_lazy(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    **edge_attrs: str,
) -> Iterator[str]:
    yield from pred_lazy(graph, n_id, depth, label_cfg='CFG', **edge_attrs)


@trace()
def paths(
    graph: Graph,
    s_id: str,
    t_id: str,
    **edge_attrs: str,
) -> Tuple[Tuple[str, ...], ...]:
    return tuple(_paths(graph, s_id, t_id, **edge_attrs))


def _paths(
    graph: Graph,
    s_id: str,
    t_id: str,
    **edge_attrs: str,
) -> Iterator[Tuple[str, ...]]:
    t_ids = {t_id}

    if s_id in t_ids:
        return

    visited: Dict[str, None] = dict.fromkeys([s_id])
    pending = [(s_id, iter(graph[s_id]))]

    while pending:
        pending_s_id, pending_ids = pending[-1]
        child = next(pending_ids, None)

        if child is None:
            pending.pop()
            visited.popitem()

        elif len(visited) + 1 < len(graph):
            if (
                # Already visited
                child in visited
                # Does not match the criteria
                or not has_labels(graph[pending_s_id][child], **edge_attrs)
            ):
                continue

            if child in t_ids:
                yield tuple(visited) + (child,)

            visited[child] = None
            if t_ids - set(visited):
                pending.append((child, iter(graph[child])))
            else:
                visited.popitem()
        else:
            for n_id in (t_ids & (set(pending_ids) | {child})) - set(visited):
                yield tuple(visited) + (n_id,)
            pending.pop()
            visited.popitem()


def get_node_cfg_condition(graph: Graph, n_id: str) -> str:
    p_id = graph.nodes[n_id]['label_parent_ast']
    val: str

    for key, val in graph[p_id][n_id].items():
        if key.startswith('label_cfg_'):
            return val

    return 'cfg_never'


def match_ast(
    graph: Graph,
    n_id: str,
    *label_type: str,
) -> Dict[str, Optional[str]]:
    index: int = 0
    nodes: Dict[str, Optional[str]] = dict.fromkeys(label_type)

    for c_id in adj_ast(graph, n_id):
        c_type = graph.nodes[c_id]['label_type']
        if c_type in nodes and nodes[c_type] is None:
            nodes[c_type] = c_id
        else:
            nodes[f'__{index}__'] = c_id
            index += 1

    return nodes


def match_ast_group(
    graph: Graph,
    n_id: str,
    *label_type: str,
) -> Dict[str, Set[str]]:
    index: int = 0
    nodes: Dict[str, Set[str]] = dict.fromkeys(label_type)

    for c_id in adj_ast(graph, n_id):
        c_type = graph.nodes[c_id]['label_type']
        if c_type in nodes:
            if not nodes[c_type]:
                nodes[c_type] = {c_id}
            else:
                nodes[c_type].add(c_id)
        else:
            nodes[f'__{index}__'] = c_id
            index += 1

    return nodes


def get_ast_childs(
    graph: Graph,
    n_id: NId,
    label_type: str,
    *,
    depth: int = 1,
) -> Tuple[NId, ...]:
    return tuple(
        n_id
        for n_id in adj_ast(graph, n_id, depth=depth)
        if graph.nodes[n_id]['label_type'] == label_type
    )


def is_connected_to_cfg(graph: Graph, n_id: NId) -> bool:
    return bool(adj_cfg(graph, n_id) or pred_cfg(graph, n_id))


def lookup_first_cfg_parent(
    graph: Graph,
    n_id: NId,
) -> str:
    # Lookup first parent who is connected to the CFG
    for p_id in chain([n_id], pred_ast_lazy(graph, n_id, depth=-1)):
        if is_connected_to_cfg(graph, p_id):
            return cast(str, p_id)

    # Base case, pass through
    return cast(str, n_id)


def flows(
    graph: Graph,
    *,
    input_type: str,
    sink_type: str,
) -> Tuple[Tuple[int, Tuple[str, ...]], ...]:
    return tuple(enumerate(sorted(
        path
        for s_id, t_id in product(
            # Inputs
            filter_nodes(
                graph,
                graph.nodes,
                pred_has_labels(label_input_type=input_type),
            ),
            # Sinks
            filter_nodes(
                graph,
                graph.nodes,
                pred_has_labels(label_sink_type=sink_type),
            ),
        )
        for path in paths(
            graph,
            lookup_first_cfg_parent(graph, s_id),
            lookup_first_cfg_parent(graph, t_id),
            label_cfg='CFG',
        )
    )))


@trace()
def branches_cfg(
    graph: Graph,
    n_id: NId,
    finding: core_model.FindingEnum
) -> Tuple[Tuple[str, ...], ...]:
    # Compute all childs reachable from CFG edges
    c_ids = adj_cfg(graph, n_id, depth=-1)

    # Filter the ones that are connected to a sink via the AST
    target_ids = tuple(
        c_id
        for c_id in c_ids
        if (
            # The node's sink match the finding name
            graph.nodes[c_id].get('label_sink_type') == finding.name
            # The node has an AST child that is a sink of the finding
            or any(
                graph.nodes[c_c_id].get('label_sink_type') == finding.name
                for c_c_id in adj_ast(graph, c_id, depth=-1)
            )
            # The node is and leaf node
            or not adj_cfg(graph, c_id)
        )
    )

    # All branches, may be duplicated, some branches may be prefix of others
    branches = set(
        (path, '-'.join(path))
        for leaf_id in target_ids
        for path in paths(graph, n_id, leaf_id, label_cfg='CFG')
    )

    # Deduplicate, merge prefixes and return branches
    return tuple(sorted(
        path
        for path, path_str in branches
        if not any(
            p_str.startswith(path_str)
            for _, p_str in branches
            if p_str != path_str
        )
    ))


def import_graph_from_json(model: Any) -> Graph:
    graph = Graph()

    for n_id, n_attrs in model['nodes'].items():
        graph.add_node(n_id, **n_attrs)

    for n_id_from, n_id_from_value in model['edges'].items():
        for n_id_to, edge_attrs in n_id_from_value.items():
            graph.add_edge(n_id_from, n_id_to, **edge_attrs)

    return graph


def export_graph_as_json(
    graph: Graph,
    *,
    include_styles: bool = False,
) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    data['nodes'] = {}
    data['edges'] = {}
    ignored_attrs = GRAPH_STYLE_ATTRS

    for n_id, n_attrs in graph.nodes.items():
        data['nodes'][n_id] = n_attrs.copy()

        if not include_styles:
            for attr in ignored_attrs:
                data['nodes'][n_id].pop(attr, None)

    for n_id_from, n_id_to in graph.edges:
        data['edges'].setdefault(n_id_from, {})
        data['edges'][n_id_from][n_id_to] = graph[n_id_from][n_id_to].copy()

        if not include_styles:
            for attr in ignored_attrs:
                data['edges'][n_id_from][n_id_to].pop(attr, None)

    return data


def _get_subgraph(
    graph: Graph,
    node_n_id_predicate: NIdPredicateFunction = lambda n_id: True,
    edge_n_attrs_predicate: NAttrsPredicateFunction = lambda n_attrs: True,
) -> Graph:
    copy: Graph = Graph()

    for n_a_id, n_b_id in graph.edges:
        edge_attrs = graph[n_a_id][n_b_id].copy()
        n_a_attrs = graph.nodes[n_a_id].copy()
        n_b_attrs = graph.nodes[n_b_id].copy()

        if (
            edge_n_attrs_predicate(edge_attrs)
            and node_n_id_predicate(n_a_id)
            and node_n_id_predicate(n_b_id)
        ):
            copy.add_node(n_a_id, **n_a_attrs)
            copy.add_node(n_b_id, **n_b_attrs)
            copy.add_edge(n_a_id, n_b_id, **edge_attrs)

    return copy


def copy_ast(graph: Graph) -> Graph:
    return _get_subgraph(
        graph=graph,
        edge_n_attrs_predicate=pred_has_labels(label_ast='AST'),
    )


def copy_cfg(graph: Graph) -> Graph:
    return _get_subgraph(
        graph=graph,
        edge_n_attrs_predicate=pred_has_labels(label_cfg='CFG'),
    )


def contains_label_type_in(
    graph: Graph,
    c_ids: Tuple[str, ...],
    label_types: Set[str],
) -> bool:
    return all(
        graph.nodes[c_id].get('label_type') in label_types
        for c_id in c_ids
    )


def concatenate_label_text(
    graph: Graph,
    c_ids: Tuple[str, ...],
) -> str:
    return ''.join(graph.nodes[c_id]['label_text'] for c_id in c_ids)


# Functions below should disappear


def symbolic_evaluate(value: Any) -> Any:
    """Evaluate a list of expressions, return a possibly simplified equivalent.

    Examples:

        >>> [StringLiteral, ADD, StringLiteral, ADD, StringLiteral]
        StringLiteral
    """
    # Only a list of expressions can be evaluated
    if not isinstance(value, list):
        return value

    # Recursively simplify the element
    value = list(map(symbolic_evaluate, value))

    # Value is composed from 'StringLiterals' joined by 'ADD'
    if set(jsh('[0::2].type', value)) == {'StringLiteral'} \
            and set(jsh('[1::2].type', value)) == {'ADD'}:
        final = value[0]
        final['text'] = '"' + ''.join(t['text'][1:-1] for t in value) + '"'
        return final

    return value


def simplify(value: Any) -> Any:
    """Access single node elements in order to flatten a graph.

    Examples:

        >>> simplify([{'a': 1}]) == {'a': 1}

        >>> simplify({'a': []}) == []
    """
    if isinstance(value, list):
        if len(value) == 1:
            return simplify(value[0])
        return list(map(simplify, value))

    if isinstance(value, dict):
        if len(value) == 1:
            child_val, = value.values()
            return simplify(child_val)
        return dict(zip(value.keys(), map(simplify, value.values())))

    return value


def yield_nodes_with_key(*, key: str, node: Any) -> Iterator[Any]:
    yield from yield_nodes(
        key_predicates=(key.__eq__,),
        post_extraction=(),
        pre_extraction=(),
        value=node,
    )


def yield_nodes(
    *,
    key: str = '__root__',
    value: Any,
    key_predicates: Tuple[Callable[[str], bool], ...] = (),
    value_extraction: str = '@',
    value_predicates: Tuple[str, ...] = (),
    pre_extraction: Tuple[Callable[[Any], Any], ...] = (
        simplify,
        symbolic_evaluate,
    ),
    post_extraction: Tuple[Callable[[Any], Any], ...] = (
        simplify,
        symbolic_evaluate,
    ),
) -> Iterator[Any]:
    """Recursively scan the graph and yield nodes that match the predicates."""

    def _yield_if_matches() -> Iterator[Any]:
        if all(jsh(pred, value) for pred in value_predicates) \
                and all(pred(key) for pred in key_predicates):
            to_yield = value
            for action in pre_extraction:
                to_yield = action(to_yield)
            to_yield = jsh(value_extraction, to_yield)
            for action in post_extraction:
                to_yield = action(to_yield)
            yield to_yield

    if isinstance(value, dict):
        yield from _yield_if_matches()
        for child_key, child_value in value.items():
            yield from yield_nodes(
                key=child_key,
                value=child_value,
                key_predicates=key_predicates,
                post_extraction=post_extraction,
                pre_extraction=pre_extraction,
                value_extraction=value_extraction,
                value_predicates=value_predicates,
            )
    elif isinstance(value, list):
        yield from _yield_if_matches()
        for child_key, child_value in enumerate(value):
            yield from yield_nodes(
                key=f'{key}[{child_key}]',
                value=child_value,
                key_predicates=key_predicates,
                post_extraction=post_extraction,
                pre_extraction=pre_extraction,
                value_extraction=value_extraction,
                value_predicates=value_predicates,
            )


def yield_dicts(model: Any) -> Iterator[Dict[str, Any]]:
    if isinstance(model, dict):
        yield model
        for sub_model in model.values():
            yield from yield_dicts(sub_model)
    elif isinstance(model, list):
        for sub_model in model:
            yield from yield_dicts(sub_model)


def yield_object_creation_expression(
    graph: Graph,
    identifiers: Set[str],
) -> Iterator[str]:
    for n_id in filter_nodes(
            graph,
            graph.nodes,
            predicate=pred_has_labels(
                label_type='object_creation_expression'),
    ):
        match = match_ast(
            graph,
            n_id,
            'new',
            'scoped_type_identifier',
            'argument_list',
            'type_identifier',
        )
        if (len(match) == 4
                and ((class_id := match['scoped_type_identifier']) or
                     (class_id := match['type_identifier']))
                and graph.nodes[class_id]['label_text'] in identifiers):
            yield n_id
