# Standard library
from typing import (
    Any,
    Dict,
    Callable,
    Iterable,
    Iterator,
    List,
    Tuple,
)

# Third party libraries
from aioextensions import (
    collect,
)
from jmespath import (
    search as jsh,
)
import networkx as nx

# Local libraries
from utils.system import (
    read,
)

# Constants
GRAPH_STYLE_ATTRS = {'arrowhead', 'color', 'fillcolor', 'label', 'style'}

# Types
NAttrs = Dict[str, str]
NAttrsPredicateFunction = Callable[[NAttrs], bool]


async def _to_svg(graph: nx.OrderedDiGraph, path: str) -> bool:
    nx.drawing.nx_agraph.write_dot(graph, path)

    code, stdout, stderr = await read('dot', '-O', '-T', 'svg', path)

    if code == 0:
        return True

    raise SystemError(f'stdout: {stdout.decode()}, stderr: {stderr.decode()}')


async def to_svg(graph: nx.OrderedDiGraph, path: str) -> bool:
    return all(await collect((
        _to_svg(graph, path),
        _to_svg(copy_ast(graph), f'{path}.ast'),
        _to_svg(copy_cfg(graph), f'{path}.cfg'),
    )))


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
    graph: nx.OrderedDiGraph,
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
    graph: nx.OrderedDiGraph,
    n_id: str,
    depth: int = 1,
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
                results.extend(adj(graph, c_id, depth=depth - 1, **edge_attrs))

    return tuple(results)


def pred(
    graph: nx.OrderedDiGraph,
    n_id: str,
    depth: int = 1,
    **edge_attrs: str,
) -> Tuple[str, ...]:
    """Same as `adj` but follow edges in the opposite direction."""
    if depth == 0:
        return ()

    results: List[str] = []

    p_ids: List[str] = sorted(graph.pred[n_id], key=int)

    # Append direct parents
    for p_id in p_ids:
        if has_labels(graph[p_id][n_id], **edge_attrs):
            results.append(p_id)

    # Recurse into parents
    if depth < 0 or depth > 1:
        for p_id in p_ids:
            if has_labels(graph[p_id][n_id], **edge_attrs):
                results.extend(
                    pred(graph, p_id, depth=depth - 1, **edge_attrs),
                )

    return tuple(results)


def import_graph_from_json(model: Any) -> nx.OrderedDiGraph:
    graph = nx.OrderedDiGraph()

    for n_id, n_attrs in model['nodes'].items():
        graph.add_node(n_id, **n_attrs)

    for n_id_from, n_id_from_value in model['edges'].items():
        for n_id_to, edge_attrs in n_id_from_value.items():
            graph.add_edge(n_id_from, n_id_to, **edge_attrs)

    return graph


def export_graph_as_json(
    graph: nx.OrderedDiGraph,
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
    graph: nx.OrderedDiGraph,
    node_predicate: NAttrsPredicateFunction = lambda n_attrs: True,
    edge_predicate: NAttrsPredicateFunction = lambda n_attrs: True,
) -> nx.OrderedDiGraph:
    copy: nx.OrderedDiGraph = nx.OrderedDiGraph()

    for n_a_id, n_b_id in graph.edges:
        edge_attrs = graph[n_a_id][n_b_id].copy()
        n_a_attrs = graph.nodes[n_a_id].copy()
        n_b_attrs = graph.nodes[n_b_id].copy()

        if (
            edge_predicate(edge_attrs)
            and node_predicate(n_a_attrs)
            and node_predicate(n_b_attrs)
        ):
            copy.add_node(n_a_id, **n_a_attrs)
            copy.add_node(n_b_id, **n_b_attrs)
            copy.add_edge(n_a_id, n_b_id, **edge_attrs)

    return copy


def copy_ast(graph: nx.OrderedDiGraph) -> nx.OrderedDiGraph:
    return _get_subgraph(
        graph=graph,
        edge_predicate=pred_has_labels(label_ast='AST'),
    )


def copy_cfg(graph: nx.OrderedDiGraph) -> nx.OrderedDiGraph:
    return _get_subgraph(
        graph=graph,
        edge_predicate=pred_has_labels(label_cfg='CFG'),
    )


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
