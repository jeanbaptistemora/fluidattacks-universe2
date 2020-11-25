"""Modify in-place sub-trees of the graph in order to simplify it."""

# Standard library
from typing import (
    Callable,
    Dict,
    Iterable,
    List,
    Set,
    Tuple,
)

# Third party libraries
import networkx as nx

# Local libraries
from utils import (
    graph as g,
)


def _patch_node_types(graph: nx.OrderedDiGraph) -> None:
    for n_attrs in graph.nodes.values():
        label_type: str = n_attrs['label_type']

        try:
            # Input format is regularly Name|index
            label_type, label_type_index = label_type.rsplit('|', maxsplit=1)

            n_attrs['label_type'] = label_type
            n_attrs['label_type_index'] = label_type_index
        except ValueError:
            # Some literal nodes have not the index
            n_attrs['label_type'] = label_type
            n_attrs['label_type_index'] = '0'


def _join_label_texts(graph: nx.OrderedDiGraph, n_ids: Iterable[str]) -> str:
    return ''.join(graph.nodes[n_id]['label_text'] for n_id in n_ids)


def _concatenate_child_texts_in_place(
    graph: nx.OrderedDiGraph,
    n_attrs_label_type: str,
    n_ids: List[str],
) -> None:
    graph.nodes[n_ids[0]]['label_text'] = _join_label_texts(graph, n_ids)
    graph.nodes[n_ids[0]]['label_type'] = n_attrs_label_type
    graph.remove_nodes_from(n_ids[1:])


def _concatenate_child_texts(
    graph: nx.OrderedDiGraph,
    parent_label_type: str,
    childs_label_types: Tuple[str, ...],
) -> None:
    nodes_to_process = g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type=parent_label_type,
    ))

    nodes_to_edit: List[str] = [
        n_id
        for n_id in nodes_to_process
        for c_ids in [g.adj(graph, n_id)]
        if len(c_ids) == len(childs_label_types)
        and all(
            graph.nodes[c_id]['label_type'] == child_label_type
            for c_id, child_label_type in zip(c_ids, childs_label_types)
        )
    ]

    for n_id in nodes_to_edit:
        c_ids = g.adj(graph, n_id)
        n_attrs = graph.nodes[n_id]
        n_attrs['label_type'] = f'Custom{parent_label_type}'
        n_attrs['label_text'] = _join_label_texts(graph, c_ids)
        graph.remove_nodes_from(c_ids)


def _replace_with_child(
    graph: nx.OrderedDiGraph,
    parent_label_type: str,
    childs_label_type: str,
) -> None:
    nodes_to_process = g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type=parent_label_type,
    ))

    nodes_to_edit: List[Tuple[str, str]] = [
        (n_id, c_id)
        for n_id in nodes_to_process
        for c_id in g.adj(graph, n_id)
        if graph.nodes[c_id]['label_type'] == childs_label_type
    ]

    for n_id, c_id in reversed(nodes_to_edit):
        p_id = graph.nodes[n_id]['label_parent_ast']
        graph.nodes[c_id]['label_parent_ast'] = p_id
        graph.add_edge(p_id, c_id, **graph[p_id][n_id])
        graph.remove_node(n_id)


def _reduce_ordered(
    graph: nx.OrderedDiGraph,
    parent_label_type: str,
    rules: Tuple[Tuple[str, Set[str]], ...],
    reducers: Dict[str, Callable[
        [nx.OrderedDiGraph, str, List[str]],
        None,
    ]],
) -> None:
    for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type=parent_label_type,
    )):
        rules_i = iter(rules)
        result: Dict[str, List[str]] = {}
        label_type, expected_label_types = next(rules_i)

        # Iterate all child nodes and strain them to the result dictionary
        for c_id in g.adj(graph, n_id):
            c_attrs = graph.nodes[c_id]
            c_attrs_label_type = c_attrs['label_type']

            # Check if we are still in the same group of nodes
            if c_attrs_label_type not in expected_label_types:
                try:
                    # Advance to the next group
                    label_type, expected_label_types = next(rules_i)
                except StopIteration:
                    # Nothing more to process
                    break

            # Small integrity check
            if (
                '__any__' not in expected_label_types
                and c_attrs_label_type not in expected_label_types
            ):
                # If this happens map more rules to rules_i
                raise NotImplementedError(c_attrs_label_type)

            # Append the current node to the results
            label_type = (
                c_attrs_label_type
                if label_type == '__idem__'
                else label_type
            )
            result.setdefault(label_type, [])
            result[label_type].append(c_id)

        # Process results and apply reducers to multiple-element childs
        for label_type, c_ids in result.items():
            if len(c_ids) > 1:
                reducers[label_type](graph, label_type, c_ids)


def reduce(graph: nx.OrderedDiGraph) -> None:
    _patch_node_types(graph)
    _concatenate_child_texts(graph, 'ClassType_lf_classOrInterfaceType', (
        'DOT',
        'IdentifierRule',
    ))
    _concatenate_child_texts(graph, 'ClassOrInterfaceType', (
        'IdentifierRule',
        'CustomClassType_lf_classOrInterfaceType',
    ))
    _concatenate_child_texts(graph, 'ClassType', (
        'CustomClassOrInterfaceType',
        'DOT',
        'IdentifierRule',
    ))
    _replace_with_child(graph, 'ExceptionTypeList', 'ExceptionType')
    _reduce_ordered(
        graph,
        parent_label_type='ClassInstanceCreationExpression_lfno_primary',
        rules=(
            ('NEW', {'NEW'}),
            ('CustomIdentifier', {'DOT', 'IdentifierRule'}),
            ('LPAREN', {'LPAREN'}),
            ('__idem__', {'__any__'}),
            ('RPAREN', {'RPAREN'}),
        ),
        reducers={
            'CustomIdentifier': _concatenate_child_texts_in_place,
        },
    )
