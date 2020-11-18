# Standard library
from typing import (
    Any,
    Dict,
    Callable,
    Iterator,
    Tuple,
)

# Third party libraries
from jmespath import (
    search as jsh,
)
import networkx as nx

# Local libraries
from utils.system import (
    read,
)


def export_graph(graph: nx.OrderedDiGraph, path: str) -> bool:
    # $ nix-env -i graphviz
    # $ dot -O -T svg  <path>
    # $ google-chrome <path>.svg
    nx.drawing.nx_agraph.write_dot(graph, path)

    return True


async def graphviz_to_svg(path: str) -> bool:
    code, stdout, stderr = await read('dot', '-O', '-T', 'svg', path)

    if code == 0:
        return True

    raise SystemError(f'stdout: {stdout.decode()}, stderr: {stderr.decode()}')


def has_label(data: Dict[str, Any], *labels: str) -> bool:
    if labels:
        match_labels = [
            label for key, value in data.items() for label in labels
            if key != 'label' and key.startswith('label') and value == label
        ]
        return len(labels) == len(match_labels)
    return False


def export_graph_as_json(graph: nx.OrderedDiGraph) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    data['nodes'] = {}
    data['edges'] = {}
    ignored_attrs = ['arrowhead', 'color', 'label']

    for n_id, n_attrs in graph.nodes.items():
        data['nodes'][n_id] = n_attrs.copy()
        for attr in ignored_attrs:
            data['nodes'][n_id].pop(attr, None)

    for n_id_from, n_id_to in graph.edges:
        data['edges'].setdefault(n_id_from, {})
        data['edges'][n_id_from][n_id_to] = graph[n_id_from][n_id_to].copy()
        for attr in ignored_attrs:
            data['edges'][n_id_from][n_id_to].pop(attr, None)

    return data


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
