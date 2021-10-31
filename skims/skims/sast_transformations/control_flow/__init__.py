from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage,
)
from sast_transformations.control_flow.generate import (
    generic,
)
from sast_transformations.control_flow.javascript import (
    unnamed_function as javascript_unnamed_function,
)
from sast_transformations.control_flow.types import (
    CfgArgs,
)
from utils import (
    graph as g,
)


def c_sharp_add(graph: Graph) -> None:
    def _predicate(n_attrs: str) -> bool:
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


def go_add(graph: Graph) -> None:
    def _predicate(n_id: str) -> bool:
        return g.pred_has_labels(label_type="function_declaration")(
            n_id
        ) or g.pred_has_labels(label_type="method_declaration")(n_id)

    language = GraphShardMetadataLanguage.GO

    for n_id in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=_predicate,
    ):
        generic(args=CfgArgs(generic, graph, n_id, language), stack=[])


def java_add(graph: Graph) -> None:
    def _predicate(n_id: str) -> bool:
        return (
            g.pred_has_labels(
                label_type="method_declaration",
            )(n_id)
            or g.pred_has_labels(label_type="constructor_declaration")(n_id)
        )

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

    # some nodes must be post-processed
    for n_id, node in graph.nodes.items():
        if g.pred_has_labels(label_type="arrow_function")(
            node
        ) or g.pred_has_labels(label_type="function")(node):
            args = CfgArgs(generic, graph, n_id, language)
            javascript_unnamed_function(args, stack=[])


def kotlin_add(graph: Graph) -> None:
    def _predicate(n_id: str) -> bool:
        return (
            g.pred_has_labels(label_type="function_declaration")(n_id)
            or g.pred_has_labels(label_type="class_declaration")(n_id)
            or g.pred_has_labels(label_type="companion_object")(n_id)
        )

    language = GraphShardMetadataLanguage.KOTLIN

    for n_id in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=_predicate,
    ):
        generic(args=CfgArgs(generic, graph, n_id, language), stack=[])


def add(
    graph: Graph,
    language: GraphShardMetadataLanguage,
) -> None:
    if language == GraphShardMetadataLanguage.JAVA:
        java_add(graph)
    elif language == GraphShardMetadataLanguage.JAVASCRIPT:
        javascript_add(graph)
    elif language == GraphShardMetadataLanguage.CSHARP:
        c_sharp_add(graph)
    elif language == GraphShardMetadataLanguage.GO:
        go_add(graph)
    elif language == GraphShardMetadataLanguage.KOTLIN:
        kotlin_add(graph)
