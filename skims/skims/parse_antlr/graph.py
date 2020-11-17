# Standard library
from itertools import (
    count,
)
from typing import (
    Any,
    Dict,
    Iterator,
    Optional,
)

# Third party libraries
import networkx as nx


def _node_has_position_metadata(node: Dict[str, Any]) -> bool:
    return set(node.keys()).issuperset({'c', 'l', 'text', 'type'})


def _create_label(**attrs: str) -> str:
    return '\n'.join(f'{key}: {attrs[key]}' for key in sorted(attrs))


def _create_leaf(  # pylint: disable=too-many-arguments
    counter: Iterator[int],
    graph: nx.OrderedDiGraph,
    index: int,
    key: Optional[str],
    parent: Optional[str],
    value: Any,
) -> nx.OrderedDiGraph:
    node_id: str = str(next(counter))

    # Add a new node and link it to the parent
    graph.add_node(node_id)
    if parent:
        graph.add_edge(parent, node_id, index=index)

    if isinstance(value, dict):
        if _node_has_position_metadata(value):
            for value_key, value_value in value.items():
                graph.nodes[node_id][value_key] = value_value
        else:
            graph = _build_graph(
                model=value,
                _counter=counter,
                _graph=graph,
                _parent=node_id,
            )
            graph.nodes[node_id]['type'] = key
    elif isinstance(value, list):
        graph = _build_graph(
            model=value,
            _counter=counter,
            _graph=graph,
            _parent=node_id,
        )
    else:
        # May happen?
        raise NotImplementedError()

    return graph


def _build_graph(
    model: Any,
    _counter: Optional[Iterator[int]] = None,
    _graph: Optional[nx.OrderedDiGraph] = None,
    _parent: Optional[str] = None,
) -> nx.OrderedDiGraph:
    # Handle first level of recurssion, where _graph is None
    counter = count(1) if _counter is None else _counter
    graph = nx.OrderedDiGraph() if _graph is None else _graph

    if isinstance(model, dict):
        for index, (key, value) in enumerate(model.items()):
            _create_leaf(
                counter=counter,
                graph=graph,
                index=index,
                key=key,
                parent=_parent,
                value=value,
            )
    elif isinstance(model, list):
        for index, value in enumerate(model):
            _create_leaf(
                counter=counter,
                graph=graph,
                index=index,
                key=None,
                parent=_parent,
                value=value,
            )
    else:
        # May happen?
        raise NotImplementedError()

    return graph


def _propagate_positions(graph: nx.OrderedDiGraph) -> None:
    # Iterate nodes ordered from the leaves to the root
    for n_id in nx.dfs_postorder_nodes(graph):
        # If the node has no metadata let's propagate it from the child
        if not _node_has_position_metadata(graph.nodes[n_id]):
            # This is the first child node, graph ordering guarantees it
            c_id = tuple(graph.adj[n_id])[0]

            # Propagate metadata from the child to the parent
            graph.nodes[n_id]['c'] = graph.nodes[c_id]['c']
            graph.nodes[n_id]['l'] = graph.nodes[c_id]['l']


def _add_labels(graph: nx.OrderedDiGraph) -> None:
    # Walk the nodes and compute a label from the node attributes
    for n_id, n_attrs in graph.nodes.items():
        graph.nodes[n_id]['label'] = _create_label(**n_attrs, id=n_id)

    # Walk the edges and compute a label from the edge attributes
    for n_id_u, n_id_v in graph.edges:
        graph[n_id_u][n_id_v]['label'] = _create_label(**graph[n_id_u][n_id_v])


def _colorize(graph: nx.OrderedDiGraph) -> None:
    # https://graphviz.org/doc/info/attrs.html
    # https://graphviz.org/doc/info/colors.html
    # color: border of the node, edge
    # fillcolor: fill color of the node
    # fontcolor: color of the text

    # Walk the nodes and compute a label from the node attributes
    for n_id in graph.nodes:
        graph.nodes[n_id]['color'] = 'black'

    # Walk the edges and compute a label from the edge attributes
    for n_id_u, n_id_v in graph.edges:
        graph[n_id_u][n_id_v]['color'] = 'blue'


def from_model(model: Any) -> nx.OrderedDiGraph:
    graph = _build_graph(model)

    _propagate_positions(graph)
    _add_labels(graph)
    _colorize(graph)

    return graph
