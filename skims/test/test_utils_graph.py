# Third party libraries
import networkx as nx

# Local libraries
from utils.graph import (
    yield_nodes_reachable_from_node,
)


def test_all() -> None:
    graph = nx.OrderedDiGraph()
    graph.add_node('a')
    graph.add_node('b')
    graph.add_node('c')
    graph.add_node('d')
    graph.add_edge('b', 'a')
    graph.add_edge('b', 'c')
    graph.add_edge('c', 'd')
    graph.add_edge('d', 'e')

    # b
    # - a
    # - c
    #   - d
    #     - e

    assert set(yield_nodes_reachable_from_node(graph, 'a')) == set()
    assert set(yield_nodes_reachable_from_node(graph, 'a', 1)) == set()
    assert set(yield_nodes_reachable_from_node(graph, 'b')) == {'a', 'c', 'd', 'e'}
    assert set(yield_nodes_reachable_from_node(graph, 'b', 2)) == {'a', 'c', 'd'}
    assert set(yield_nodes_reachable_from_node(graph, 'b', 1)) == {'a', 'c'}
    assert set(yield_nodes_reachable_from_node(graph, 'b', 0)) == set()
    assert set(yield_nodes_reachable_from_node(graph, 'c')) == {'d', 'e'}
    assert set(yield_nodes_reachable_from_node(graph, 'c', 1)) == {'d'}
