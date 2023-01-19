from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage,
)
from sast_transformations.control_flow.generate import (
    generic,
)
from sast_transformations.control_flow.types import (
    CfgArgs,
)
from utils import (
    graph as g,
)


def c_sharp_add(graph: Graph) -> None:
    language = GraphShardMetadataLanguage.CSHARP

    for n_id in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=g.pred_has_labels(label_type="method_declaration"),
    ):
        generic(args=CfgArgs(generic, graph, n_id, language), stack=[])


def add(
    graph: Graph,
    language: GraphShardMetadataLanguage,
) -> None:
    if language == GraphShardMetadataLanguage.CSHARP:
        c_sharp_add(graph)
