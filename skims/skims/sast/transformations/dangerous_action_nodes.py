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
    _mark_java_f004(graph)
    _mark_java_f042(graph)


def _mark_java_f063(graph: graph_model.Graph) -> None:
    _mark_java_f063_obj_creation_exp(graph)
    _mark_java_f063_method_call(graph)


def _mark_java_f063_obj_creation_exp(graph: graph_model.Graph) -> None:
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


def _mark_java_f063_method_call(graph: graph_model.Graph) -> None:
    for n_id in g.filter_nodes(graph, graph.nodes, g.pred_has_labels(
        label_type='method_invocation',
    )):
        match = g.match_ast(graph, n_id, 'field_access', 'identifier')

        if (
            (class_id := match['field_access'])
            and (method_id := match['identifier'])
        ):
            if (
                graph.nodes[class_id]['label_text'] == 'java.nio.file.Files'
                and graph.nodes[method_id]['label_text'] == 'newInputStream'
            ) or (
                graph.nodes[class_id]['label_text'] == 'java.nio.file.Paths'
                and graph.nodes[method_id]['label_text'] == 'get'
            ):
                graph.nodes[n_id]['label_sink_type'] = (
                    core_model.FindingEnum.F063_PATH_TRAVERSAL.name
                )


def _check_method_call(
    graph: graph_model.Graph,
    n_id: graph_model.NId,
    *call_identifiers: str,
) -> bool:
    """
    Check if a node is the call of the method specified in the identifiers
    """
    match = g.match_ast_group(
        graph,
        n_id,
        'identifier',
        'method_invocation',
    )
    if identifier := match.get('identifier'):
        identifiers = {
            graph.nodes[iden].get('label_text')
            for iden in identifier
        }
        if len(call_identifiers) == 1 and call_identifiers[0] in identifiers:
            return True

        if call_identifiers[-1] not in identifiers:
            return False
        for inx, call in enumerate(reversed(call_identifiers)):
            if call in identifiers and (method :=
                                        match.get('method_invocation')):
                return _check_method_call(
                    graph,
                    method.pop(),
                    *call_identifiers[:-inx + 1],
                )

    return False


def _mark_java_f034(graph: graph_model.Graph) -> None:
    for n_id in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=g.pred_has_labels(label_type='method_invocation'),
    ):
        if any((
                _check_method_call(graph, n_id, 'getSession', 'setAttribute'),
                _check_method_call(graph, n_id, 'addCookie'),
        )):
            graph.nodes[n_id]['label_sink_type'] = (
                core_model
                .FindingEnum
                .F034.name
            )


def _mark_java_f004(graph: graph_model.Graph) -> None:
    identifiers: Set[str] = {*build_attr_paths('ProcessBuilder'), }

    for n_id in g.yield_object_creation_expression(graph, identifiers):
        graph.nodes[n_id]['label_sink_type'] = (
            core_model
            .FindingEnum
            .F004
            .name
        )

    for n_id in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=g.pred_has_labels(label_type='method_invocation'),
    ):
        if any((
                _check_method_call(graph, n_id, 'exec'),
                _check_method_call(graph, n_id, 'command'),
                _check_method_call(graph, n_id, 'start'),
        )):
            graph.nodes[n_id]['label_sink_type'] = (
                core_model
                .FindingEnum
                .F004.name
            )


def _mark_java_f042(graph: graph_model.Graph) -> None:
    for n_id in g.filter_nodes(
            graph,
            graph.nodes,
            predicate=g.pred_has_labels(label_type='method_invocation'),
    ):
        if any((_check_method_call(graph, n_id, 'setSecure'), )):
            graph.nodes[n_id]['label_sink_type'] = (
                core_model
                .FindingEnum
                .F042.name
            )


def mark(
    graph: graph_model.Graph,
    language: graph_model.GraphShardMetadataLanguage,
) -> None:
    if language == graph_model.GraphShardMetadataLanguage.JAVA:
        _mark_java(graph)
