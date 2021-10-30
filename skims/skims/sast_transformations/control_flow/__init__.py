from functools import (
    partial,
)
from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage,
)
from sast_transformations.control_flow.generate import (
    args_generic,
    generic,
)
from sast_transformations.control_flow.go import (
    add as go_add,
)
from sast_transformations.control_flow.javascript import (
    add as javascript_add,
)
from sast_transformations.control_flow.kotlin import (
    add as kotlin_add,
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
        args = CfgArgs(args_generic, graph, n_id, language, g.ALWAYS)
        args_generic(args, stack=[])


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
        args = CfgArgs(args_generic, graph, n_id, language, g.ALWAYS)
        args_generic(args, stack=[])


def add(
    graph: Graph,
    language: GraphShardMetadataLanguage,
) -> None:
    lang_generic = partial(generic, language=language)

    if language == GraphShardMetadataLanguage.JAVA:
        java_add(graph)
    elif language == GraphShardMetadataLanguage.JAVASCRIPT:
        javascript_add(graph, lang_generic)
    elif language == GraphShardMetadataLanguage.CSHARP:
        c_sharp_add(graph)
    elif language == GraphShardMetadataLanguage.GO:
        go_add(graph, lang_generic)
    elif language == GraphShardMetadataLanguage.KOTLIN:
        kotlin_add(graph, lang_generic)
