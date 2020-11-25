"""Add some colors, labels and styles to make the graph human readable.

Only presentation (visual) logic should go here
"""

# Third party libraries
import networkx as nx

# Local libraries
from utils.graph import (
    GRAPH_STYLE_ATTRS,
)


def _create_label(**attrs: str) -> str:
    return '\n'.join(f'{key}: {attrs[key]}' for key in sorted(attrs))


def _verify(graph: nx.OrderedDiGraph) -> None:
    """Verify that styles attributes were not added somewhere else.

    Styles should be added in this module for maintainability.
    """
    for reserved_attr in GRAPH_STYLE_ATTRS:
        for n_attrs in graph.nodes.values():
            if reserved_attr in n_attrs:
                raise ValueError(f'{reserved_attr} must be added in styles')

        for n_id_u, n_id_v in graph.edges:
            if reserved_attr in graph[n_id_u][n_id_v]:
                raise ValueError(f'{reserved_attr} must be added in styles')


def _add_labels(graph: nx.OrderedDiGraph) -> None:
    # Walk the nodes and compute a label from the node attributes
    for n_id, n_attrs in graph.nodes.items():
        graph.nodes[n_id]['label'] = _create_label(**n_attrs, id=n_id)

    # Walk the edges and compute a label from the edge attributes
    for n_id_u, n_id_v in graph.edges:
        graph[n_id_u][n_id_v]['label'] = _create_label(**graph[n_id_u][n_id_v])


def _add_styles(graph: nx.OrderedDiGraph) -> None:
    # https://graphviz.org/doc/info/attrs.html
    # https://graphviz.org/doc/info/colors.html
    # color: border of the node, edge
    # fillcolor: fill color of the node
    # fontcolor: color of the text

    # Walk the nodes and compute a label from the node attributes
    for n_attrs in graph.nodes.values():
        n_attrs['color'] = 'black'
        n_attrs['style'] = 'filled'

        if n_attrs.get('label_input_type'):
            n_attrs['fillcolor'] = 'gold'
        elif n_attrs.get('label_sink_type'):
            n_attrs['fillcolor'] = 'orange'
        else:
            n_attrs['fillcolor'] = 'white'

    # Walk the edges and compute a label from the edge attributes
    for n_id_u, n_id_v in graph.edges:
        edge_attrs = graph[n_id_u][n_id_v]
        edge_attrs['arrowhead'] = 'open'

        if 'label_ast' in edge_attrs and 'label_cfg' in edge_attrs:
            edge_attrs['color'] = 'purple'
        elif 'label_ast' in edge_attrs:
            edge_attrs['color'] = 'blue'
        elif 'label_cfg' in edge_attrs:
            edge_attrs['color'] = 'red'
        else:
            # Should not happen
            raise NotImplementedError()


def stylize(graph: nx.OrderedDiGraph) -> None:
    _verify(graph)
    _add_labels(graph)
    _add_styles(graph)
