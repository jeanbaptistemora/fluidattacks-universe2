# Local libraries
from typing import (
    Set,
)
from model import (
    core_model,
    graph_model,
)
from sast.common import (
    build_attr_paths,
)
from utils import (
    graph as g,
)


def _mark_java(graph: graph_model.Graph) -> None:
    _mark_java_object_creation_expression(graph)


def _mark_java_object_creation_expression(graph: graph_model.Graph) -> None:
    identifiers: Set[str] = {
        *build_attr_paths('java', 'io', 'File'),
        *build_attr_paths('java', 'io', 'FileInputStream'),
        *build_attr_paths('java', 'io', 'FileOutputStream'),
    }

    for n_id in g.filter_nodes(graph, graph.nodes, predicate=g.pred_has_labels(
        label_type='object_creation_expression',
    )):
        match = g.match_ast(
            graph,
            n_id,
            'new',
            'scoped_type_identifier',
            'argument_list',
        )

        if (
            len(match) == 3
            and (class_id := match['scoped_type_identifier'])
        ):
            if graph.nodes[class_id]['label_text'] in identifiers:
                graph.nodes[n_id]['label_sink_type'] = (
                    core_model
                    .FindingEnum
                    .F063_PATH_TRAVERSAL
                    .name
                )


def mark(
    graph: graph_model.Graph,
    language: graph_model.GraphShardMetadataLanguage,
) -> None:
    if language == graph_model.GraphShardMetadataLanguage.JAVA:
        _mark_java(graph)
