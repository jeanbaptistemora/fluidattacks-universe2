from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage,
    NAttrs,
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
    def _predicate(n_attrs: NAttrs) -> bool:
        return (
            g.pred_has_labels(label_type="method_declaration")(n_attrs)
            or g.pred_has_labels(label_type="constructor_declaration")(n_attrs)
            or g.pred_has_labels(label_type="lambda_expression")(n_attrs)
        )

    language = GraphShardMetadataLanguage.CSHARP

    for n_id in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=_predicate,
    ):
        generic(args=CfgArgs(generic, graph, n_id, language), stack=[])


def java_add(graph: Graph) -> None:
    def _predicate(n_attrs: NAttrs) -> bool:
        return g.pred_has_labels(label_type="method_declaration",)(
            n_attrs
        ) or g.pred_has_labels(label_type="constructor_declaration")(n_attrs)

    language = GraphShardMetadataLanguage.JAVA

    for n_id in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=_predicate,
    ):
        generic(args=CfgArgs(generic, graph, n_id, language), stack=[])


def javascript_add(graph: Graph) -> None:
    language = GraphShardMetadataLanguage.JAVASCRIPT
    generic(args=CfgArgs(generic, graph, g.ROOT_NODE, language), stack=[])


def add(
    graph: Graph,
    language: GraphShardMetadataLanguage,
) -> None:
    if language == GraphShardMetadataLanguage.JAVA:
        java_add(graph)
    elif language == GraphShardMetadataLanguage.CSHARP:
        c_sharp_add(graph)
