# Third party libraries
import networkx as nx

# Local libraries
from utils import (
    graph as g,
)


def test_all() -> None:
    graph = nx.OrderedDiGraph()
    graph.add_node('1')
    graph.add_node('2')
    graph.add_node('3')
    graph.add_node('4')
    graph.add_node('5')
    graph.add_edge('1', '2', attr_0='b')
    graph.add_edge('1', '3', attr_0='a')
    graph.add_edge('2', '6', attr_0='b')
    graph.add_edge('3', '4', attr_0='b')
    graph.add_edge('4', '5', attr_1='a')

    # 1
    # -b-> 2
    #      -b-> 6
    # -a-> 3
    #      -b-> 4
    #           -a-> 5

    assert g.adj(graph, '1', depth=-1) == ('2', '3', '6', '4', '5')
    assert g.adj(graph, '1', depth=-1, attr_0='a') == ('3',)
    assert g.adj(graph, '1', depth=-1, attr_0='b') == ('2', '6')
    assert g.adj(graph, '1', depth=+0) == ()
    assert g.adj(graph, '1', depth=+1) == ('2', '3')
    assert g.adj(graph, '1', depth=+1, attr_0='a') == ('3',)
    assert g.adj(graph, '1', depth=+1, attr_0='b') == ('2',)
    assert g.adj(graph, '1', depth=+1, attr_1='b') == ()
