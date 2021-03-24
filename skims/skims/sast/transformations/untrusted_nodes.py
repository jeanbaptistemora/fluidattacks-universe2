# Standar libraries
from typing import (
    Set,
)

# Local libraries
from model import (
    core_model,
    graph_model,
)
from utils import (
    graph as g,
)
from sast.common import (
    build_attr_paths,
)


def _append_label_input(
    graph: graph_model.Graph,
    n_id: str,
    label: str,
) -> None:
    if sink := graph.nodes[n_id].get('label_input_type'):
        sink += f',{label}'
        graph.nodes[n_id]['label_input_type'] = sink
    else:
        graph.nodes[n_id]['label_input_type'] = label


def _mark_java(graph: graph_model.Graph) -> None:
    _mark_java_request(graph)
    _mark_java_f034(graph)


def _mark_java_request(graph: graph_model.Graph) -> None:
    findins_no_trust_requests = (
        core_model.FindingEnum.F001_JAVA_SQL.name,
        core_model.FindingEnum.F004.name,
        core_model.FindingEnum.F042.name,
        core_model.FindingEnum.F063_PATH_TRAVERSAL.name,
    )
    untrusted_types = {
        'HttpServletRequest',
    }
    for n_id in g.filter_nodes(
            graph,
            graph.nodes,
            predicate=g.pred_has_labels(label_type='method_declaration'),
    ):
        for params_id in g.get_ast_childs(graph, n_id, 'formal_parameters'):
            for param_id in g.get_ast_childs(
                    graph,
                    params_id,
                    'formal_parameter',
            ):
                untrusted_params = (type_id for type_id in g.get_ast_childs(
                    graph,
                    param_id,
                    'type_identifier',
                ) if graph.nodes[type_id]['label_text'] in untrusted_types)
                for var_type_id in untrusted_params:
                    for finding in findins_no_trust_requests:
                        _append_label_input(
                            graph,
                            var_type_id,
                            finding,
                        )


def _mark_java_f034(graph: graph_model.Graph) -> None:
    identifier_objects: Set[str] = {
        *build_attr_paths('java', 'util', 'Random'),
    }
    identifier_methos: Set[str] = {
        *build_attr_paths('java', 'lang', 'Math'),
    }

    for n_id in g.yield_object_creation_expression(graph, identifier_objects):
        graph.nodes[n_id][
            'label_input_type'] = core_model.FindingEnum.F034.name

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
                graph.nodes[n_id]['label_input_type'] = (
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
                graph.nodes[n_id]['label_input_type'] = (
                    core_model
                    .FindingEnum
                    .F034
                    .name
                )

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
