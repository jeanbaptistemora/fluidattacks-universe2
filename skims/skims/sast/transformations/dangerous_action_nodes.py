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
    _mark_java_f063(graph)
    _mark_java_f034(graph)


def _mark_java_f063(graph: graph_model.Graph) -> None:
    identifiers: Set[str] = {
        *build_attr_paths('java', 'io', 'File'),
        *build_attr_paths('java', 'io', 'FileInputStream'),
        *build_attr_paths('java', 'io', 'FileOutputStream'),
    }

    for n_id in g.yield_object_creation_expression(graph, identifiers):
        graph.nodes[n_id]['label_sink_type'] = (
            core_model
            .FindingEnum
            .F063_PATH_TRAVERSAL
            .name
        )


def _mark_java_f034(graph: graph_model.Graph) -> None:
    identifiers: Set[str] = {
        *build_attr_paths('javax', 'servlet', 'http', 'Cookie'),
    }

    for n_id in g.yield_object_creation_expression(graph, identifiers):
        graph.nodes[n_id]['label_sink_type'] = (
            core_model
            .FindingEnum
            .F034
            .name
        )

    for n_id in g.filter_nodes(
            graph,
            graph.nodes,
            predicate=g.pred_has_labels(
                label_type='method_invocation',
            )
    ):
        match = g.match_ast_group(
            graph,
            n_id,
            'identifier',
        )
        if identifier := match.get('identifier'):
            identifiers = {
                graph.nodes[iden].get('label_text')
                for iden in identifier
            }
            if len(identifiers) < 2:
                continue
            if 'addCookie' in identifiers:
                graph.nodes[n_id]['label_sink_type'] = (
                    core_model
                    .FindingEnum
                    .F034
                    .name
                )


def mark(
    graph: graph_model.Graph,
    language: graph_model.GraphShardMetadataLanguage,
) -> None:
    if language == graph_model.GraphShardMetadataLanguage.JAVA:
        _mark_java(graph)
