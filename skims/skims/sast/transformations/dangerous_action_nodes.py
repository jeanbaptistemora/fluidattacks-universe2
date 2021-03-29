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
    get_dependencies,
)
from utils import (
    graph as g,
)


def _append_label_skink(
    graph: graph_model.Graph,
    n_id: str,
    finding: core_model.FindingEnum,
) -> None:
    if 'label_sink_type' in graph.nodes[n_id]:
        graph.nodes[n_id]['label_sink_type'] += f',{finding.name}'
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
    _mark_java_methods(core_model.FindingEnum.F004, graph, syntax, {
        'command',
        'exec',
        'start',
    })
    _mark_java_methods(core_model.FindingEnum.F008, graph, syntax, {
        'format',
        'getWriter.format',
        'getWriter.print',
        'getWriter.printf',
        'getWriter.println',
        'getWriter.write',
    })
    _mark_java_methods(core_model.FindingEnum.F021, graph, syntax, {
        'compile',
        'evaluate',
    })
    _mark_java_methods(core_model.FindingEnum.F034, graph, syntax, {
        'getSession.setAttribute',
        'addCookie',
    })
    _mark_java_methods(core_model.FindingEnum.F042, graph, syntax, {
        'addCookie',
        'evaluate',
    })
    _mark_java_methods(core_model.FindingEnum.F063_TRUSTBOUND, graph, syntax, {
        'putValue',
        'setAttribute',
    })
    _mark_java_methods(core_model.FindingEnum.F107, graph, syntax, {
        'search',
    })
    _mark_java_obj(core_model.FindingEnum.F004, graph, syntax, {
        *build_attr_paths('java', 'lang', 'ProcessBuilder'),
    })
    _mark_java_obj(core_model.FindingEnum.F063_PATH_TRAVERSAL, graph, syntax, {
        *build_attr_paths('java', 'io', 'File'),
        *build_attr_paths('java', 'io', 'FileInputStream'),
        *build_attr_paths('java', 'io', 'FileOutputStream'),
    })
    _mark_java_f063_pt_method_call(graph)


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


def _mark_java_methods(
    finding: core_model.FindingEnum,
    graph: graph_model.Graph,
    graph_syntax: graph_model.SyntaxSteps,
    dangerous_methods: Set[str],
) -> None:
    for syntax_steps in graph_syntax.values():
        for index, syntax_step in enumerate(syntax_steps):
            if isinstance(syntax_step, (
                graph_model.SyntaxStepMethodInvocation,
                graph_model.SyntaxStepMethodInvocationChain,
            )):
                method = syntax_step.method.rsplit('.', maxsplit=1)[-1]

                if method in dangerous_methods:
                    _append_label_skink(graph, syntax_step.meta.n_id, finding)
                    continue

            if isinstance(syntax_step, (
                graph_model.SyntaxStepMethodInvocationChain,
            )):
                *_, parent = get_dependencies(index, syntax_steps)

                if isinstance(parent, graph_model.SyntaxStepMethodInvocation):
                    parent_method = parent.method.rsplit('.', maxsplit=1)[-1]
                    method = parent_method + '.' + method

                if method in dangerous_methods:
                    _append_label_skink(graph, syntax_step.meta.n_id, finding)


def _mark_java_obj(
    finding: core_model.FindingEnum,
    graph: graph_model.Graph,
    graph_syntax: graph_model.SyntaxSteps,
    dangerous_types: Set[str],
) -> None:
    for syntax_steps in graph_syntax.values():
        for syntax_step in syntax_steps:
            if isinstance(syntax_step, (
                graph_model.SyntaxStepObjectInstantiation,
            )):
                if syntax_step.object_type in dangerous_types:
                    _append_label_skink(graph, syntax_step.meta.n_id, finding)


def mark(
    graph: graph_model.Graph,
    language: graph_model.GraphShardMetadataLanguage,
    syntax: graph_model.GraphSyntax,
) -> None:
    if language == graph_model.GraphShardMetadataLanguage.JAVA:
        _mark_java(graph, syntax)
