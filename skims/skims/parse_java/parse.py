# Standard library
from typing import (
    Any,
)

# Third party libraries
import networkx as nx

# Local libraries
from parse_antlr.graph import (
    from_model as graph_from_antlr_model,
)
from parse_java.graph.control_flow import (
    analyze as analyze_control_flow,
)
from parse_java.graph.inputs import (
    mark as mark_inputs,
)
from parse_java.graph.reducers import (
    reduce as reduce_graph,
)
from parse_java.graph.styles import (
    stylize,
)


def from_antlr_graph(graph: nx.OrderedDiGraph) -> None:
    reduce_graph(graph)
    mark_inputs(graph)
    analyze_control_flow(graph)
    stylize(graph)


def from_antlr_model(model: Any) -> nx.OrderedDiGraph:
    graph = graph_from_antlr_model(model)

    from_antlr_graph(graph)

    return graph
