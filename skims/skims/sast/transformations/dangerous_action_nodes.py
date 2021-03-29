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


def _append_label_skink(
    graph: graph_model.Graph,
    n_id: str,
    finding: core_model.FindingEnum,
) -> None:
    if sink := graph.nodes[n_id].get('label_sink_type'):
        sink += f',{finding.name}'
        graph.nodes[n_id]['label_sink_type'] = sink
    else:
        graph.nodes[n_id]['label_sink_type'] = finding.name


def _mark_java(
    graph: graph_model.Graph,
    syntax: graph_model.GraphSyntax,
) -> None:
    _mark_java_methods(core_model.FindingEnum.F001_JAVA_SQL, graph, syntax, {
        'addBatch',
        'batchUpdate',
        'execute',
        'executeBatch',
        'executeLargeBatch',
        'executeLargeUpdate',
        'executeQuery',
        'executeUpdate',
        'query',
        'queryForInt',
        'queryForList',
        'queryForLong',
        'queryForMap',
        'queryForObject',
        'queryForRowSet',
    })
    _mark_java_f004_objects(graph)
    _mark_java_methods(core_model.FindingEnum.F004, graph, syntax, {
        'command',
        'exec',
        'start',
    })
    _mark_java_f008(graph)
    _mark_java_methods(core_model.FindingEnum.F021, graph, syntax, {
        'compile',
        'evaluate',
    })
    _mark_java_f034(graph)
    _mark_java_methods(core_model.FindingEnum.F042, graph, syntax, {
        'addCookie',
        'evaluate',
    })
    _mark_java_f063_pt(graph)
    _mark_java_methods(core_model.FindingEnum.F063_TRUSTBOUND, graph, syntax, {
        'putValue',
        'setAttribute',
    })
    _mark_java_methods(core_model.FindingEnum.F107, graph, syntax, {
        'search',
    })


def _mark_java_f004_objects(graph: graph_model.Graph) -> None:
    identifiers: Set[str] = {
        *build_attr_paths('java', 'lang', 'ProcessBuilder'),
    }

    for n_id in g.yield_object_creation_expression(graph, identifiers):
        graph.nodes[n_id]['label_sink_type'] = (
            core_model
            .FindingEnum
            .F004
            .name
        )


def _mark_java_f008(graph: graph_model.Graph) -> None:
    for n_id in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=g.pred_has_labels(label_type='method_invocation'),
    ):
        if any((
                _check_method_call(graph, n_id, 'format'),
                _check_method_call(graph, n_id, 'getWriter', 'format'),
                _check_method_call(graph, n_id, 'getWriter', 'print'),
                _check_method_call(graph, n_id, 'getWriter', 'printf'),
                _check_method_call(graph, n_id, 'getWriter', 'println'),
                _check_method_call(graph, n_id, 'getWriter', 'write'),
        )):
            _append_label_skink(graph, n_id, core_model.FindingEnum.F008)


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
            _append_label_skink(graph, n_id, core_model.FindingEnum.F034)


def _mark_java_f063_pt(graph: graph_model.Graph) -> None:
    _mark_java_f063_pt_obj_creation_exp(graph)
    _mark_java_f063_pt_method_call(graph)


def _mark_java_f063_pt_obj_creation_exp(graph: graph_model.Graph) -> None:
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


def _mark_java_f063_pt_method_call(graph: graph_model.Graph) -> None:
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


def _mark_java_methods(
    finding: core_model.FindingEnum,
    graph: graph_model.Graph,
    graph_syntax: graph_model.SyntaxSteps,
    dangerous_methods: Set[str],
) -> None:
    for syntax_steps in graph_syntax.values():
        for syntax_step in syntax_steps:
            if isinstance(syntax_step, (
                graph_model.SyntaxStepMethodInvocation,
                graph_model.SyntaxStepMethodInvocationChain,
            )):
                method = syntax_step.method.rsplit('.', maxsplit=1)[-1]
                if method in dangerous_methods:
                    _append_label_skink(graph, syntax_step.meta.n_id, finding)


def mark(
    graph: graph_model.Graph,
    language: graph_model.GraphShardMetadataLanguage,
    syntax: graph_model.GraphSyntax,
) -> None:
    if language == graph_model.GraphShardMetadataLanguage.JAVA:
        _mark_java(graph, syntax)
