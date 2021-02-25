# Local libraries
from typing import (
    Iterator,
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


def _yield_object_creation_expression(
    graph: graph_model.Graph,
    identifiers: Set[str],
) -> Iterator[str]:
    for n_id in g.filter_nodes(
            graph,
            graph.nodes,
            predicate=g.pred_has_labels(
                label_type='object_creation_expression'),
    ):
        match = g.match_ast(
            graph,
            n_id,
            'new',
            'scoped_type_identifier',
            'argument_list',
        )

        if (len(match) == 3 and (class_id := match['scoped_type_identifier'])
                and graph.nodes[class_id]['label_text'] in identifiers):
            yield n_id


def _mark_java_f063(graph: graph_model.Graph) -> None:
    identifiers: Set[str] = {
        *build_attr_paths('java', 'io', 'File'),
        *build_attr_paths('java', 'io', 'FileInputStream'),
        *build_attr_paths('java', 'io', 'FileOutputStream'),
    }

    for n_id in _yield_object_creation_expression(graph, identifiers):
        graph.nodes[n_id]['label_sink_type'] = (
            core_model
            .FindingEnum
            .F063_PATH_TRAVERSAL
            .name
        )


def _mark_java_f034(graph: graph_model.Graph) -> None:
    identifier_objects: Set[str] = {
        *build_attr_paths('java', 'util', 'Random'),
    }
    identifier_methos: Set[str] = {
        *build_attr_paths('java', 'lang', 'Math'),
    }

    for n_id in _yield_object_creation_expression(graph, identifier_objects):
        graph.nodes[n_id]['label_sink_type'] = core_model.FindingEnum.F034.name

    for n_id in g.filter_nodes(
            graph,
            graph.nodes,
            predicate=g.pred_has_labels(label_type='method_invocation'),
    ):
        match = g.match_ast_group(
            graph,
            n_id,
            'field_access',
            'identifier',
            'argument_list',
        )
        if (field_access := match['field_access']) and len(field_access) == 1:
            if graph.nodes[list(field_access)
                           [0]]['label_text'] in identifier_methos:
                graph.nodes[n_id]['label_sink_type'] = (
                    core_model
                    .FindingEnum
                    .F034
                    .name
                )
        elif (identifier := match.get('identifier', list())) and len(
                identifier) > 1:
            identifiers = {
                graph.nodes[iden].get('label_text')
                for iden in identifier
            }
            if identifier_methos.intersection(identifiers):
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
