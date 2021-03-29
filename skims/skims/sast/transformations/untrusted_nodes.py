# Local libraries
from model import (
    core_model,
    graph_model,
)
from utils import (
    graph as g,
)


def _mark_java(graph: graph_model.Graph) -> None:
    _mark_java_f034(graph)


def _mark_java_f034(graph: graph_model.Graph) -> None:
    for n_id in g.filter_nodes(
            graph,
            graph.nodes,
            predicate=g.pred_has_labels(
                label_type='array_creation_expression'),
    ):
        match = g.match_ast(
            graph,
            n_id,
            '__1__',
        )
        if array_type := match['__1__']:
            if graph.nodes[array_type].get('label_text') == 'byte':
                graph.nodes[n_id][
                    'label_input_type'] = core_model.FindingEnum.F034.name


def mark(
    graph: graph_model.Graph,
    language: graph_model.GraphShardMetadataLanguage,
) -> None:
    if language == graph_model.GraphShardMetadataLanguage.JAVA:
        _mark_java(graph)
