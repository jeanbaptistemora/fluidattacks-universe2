# Local libraries
from model import (
    core_model,
    graph_model,
)
from utils import (
    graph as g,
)


def _mark_java(graph: graph_model.Graph) -> None:
    for n_id in g.filter_nodes(graph, graph.nodes, predicate=g.pred_has_labels(
        label_type='method_declaration',
    )):
        _mark_java_method_declaration(graph, n_id)


def _mark_java_method_declaration(
    graph: graph_model.Graph,
    n_id: graph_model.NId,
) -> None:
    for params_id in g.get_ast_childs(graph, n_id, 'formal_parameters'):
        for param_id in g.get_ast_childs(graph, params_id, 'formal_parameter'):
            for var_type_id in g.get_ast_childs(
                graph, param_id, 'type_identifier',
            ):
                var_type_n_attrs = graph.nodes[var_type_id]

                if var_type_n_attrs['label_text'] in {
                    'HttpServletRequest',
                }:
                    var_type_n_attrs['label_input_type'] = (
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
