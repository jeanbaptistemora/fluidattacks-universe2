# Local libraries
from typing import (
    Callable,
    Set,
)
from model import (
    core_model,
    graph_model,
)
from sast_syntax_readers.utils_generic import (
    get_dependencies,
)
from utils.string import (
    build_attr_paths,
)


def _append_label(
    graph: graph_model.Graph,
    n_id: str,
    label: str,
    finding: core_model.FindingEnum,
) -> None:
    if label in graph.nodes[n_id]:
        graph.nodes[n_id][label] += f',{finding.name}'
    else:
        graph.nodes[n_id][label] = finding.name


AppendLabelType = Callable[
    [graph_model.Graph, str, core_model.FindingEnum],
    None
]


def _append_label_input(
    graph: graph_model.Graph,
    n_id: str,
    finding: core_model.FindingEnum,
) -> None:
    _append_label(graph, n_id, 'label_input_type', finding)


def _append_label_sink(
    graph: graph_model.Graph,
    n_id: str,
    finding: core_model.FindingEnum,
) -> None:
    _append_label(graph, n_id, 'label_sink_type', finding)


def _mark_java_inputs(
    graph: graph_model.Graph,
    syntax: graph_model.GraphSyntax,
) -> None:
    findings = core_model.FindingEnum

    _mark_array_input(findings.F034, graph, syntax, {
        'byte',
    })
    for finding in (
        findings.F001_JAVA_SQL,
        findings.F004,
        findings.F008,
        findings.F021,
        findings.F042,
        findings.F063_PATH_TRAVERSAL,
        findings.F063_TRUSTBOUND,
        findings.F107,
    ):
        _mark_function_arg(finding, graph, syntax, build_attr_paths(
            'javax', 'servlet', 'http', 'HttpServletRequest',
        ))
    _mark_methods_input(findings.F034, graph, syntax, {
        'java.lang.Math.random',
    })
    _mark_obj_inst_input(findings.F034, graph, syntax, {
        *build_attr_paths('java', 'util', 'Random'),
    })


def _mark_java_sinks(
    graph: graph_model.Graph,
    syntax: graph_model.GraphSyntax,
) -> None:
    findings = core_model.FindingEnum

    _mark_methods_sink(findings.F001_JAVA_SQL, graph, syntax, {
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
    _mark_methods_sink(findings.F004, graph, syntax, {
        'command',
        'exec',
        'start',
    })
    _mark_methods_sink(findings.F008, graph, syntax, {
        'format',
        'getWriter.format',
        'getWriter.print',
        'getWriter.printf',
        'getWriter.println',
        'getWriter.write',
    })
    _mark_methods_sink(findings.F021, graph, syntax, {
        'compile',
        'evaluate',
    })
    _mark_methods_sink(findings.F034, graph, syntax, {
        'getSession.setAttribute',
        'addCookie',
    })
    _mark_methods_sink(findings.F042, graph, syntax, {
        'addCookie',
        'evaluate',
    })
    _mark_methods_sink(findings.F063_PATH_TRAVERSAL, graph, syntax, {
        'java.nio.file.Files.newInputStream',
        'java.nio.file.Paths.get',
    })
    _mark_methods_sink(findings.F063_TRUSTBOUND, graph, syntax, {
        'putValue',
        'setAttribute',
    })
    _mark_methods_sink(findings.F107, graph, syntax, {
        'search',
    })
    _mark_obj_inst_sink(findings.F004, graph, syntax, {
        *build_attr_paths('java', 'lang', 'ProcessBuilder'),
    })
    _mark_obj_inst_sink(findings.F063_PATH_TRAVERSAL, graph, syntax, {
        *build_attr_paths('java', 'io', 'File'),
        *build_attr_paths('java', 'io', 'FileInputStream'),
        *build_attr_paths('java', 'io', 'FileOutputStream'),
    })


def _mark_array(
    finding: core_model.FindingEnum,
    graph: graph_model.Graph,
    graph_syntax: graph_model.SyntaxSteps,
    types: Set[str],
    marker: AppendLabelType,
) -> None:
    for syntax_steps in graph_syntax.values():
        for syntax_step in syntax_steps:
            if isinstance(syntax_step, (
                graph_model.SyntaxStepArrayInstantiation,
            )):
                if syntax_step.array_type in types:
                    marker(graph, syntax_step.meta.n_id, finding)
                    continue


def _mark_array_input(
    finding: core_model.FindingEnum,
    graph: graph_model.Graph,
    graph_syntax: graph_model.SyntaxSteps,
    types: Set[str],
) -> None:
    _mark_array(
        finding,
        graph,
        graph_syntax,
        types,
        _append_label_input,
    )


def _mark_function_arg(
    finding: core_model.FindingEnum,
    graph: graph_model.Graph,
    graph_syntax: graph_model.SyntaxSteps,
    dangerous_types: Set[str],
) -> None:
    for syntax_steps in graph_syntax.values():
        for syntax_step in syntax_steps:
            if isinstance(syntax_step, graph_model.SyntaxStepDeclaration):
                if syntax_step.var_type in dangerous_types:
                    _append_label_input(graph, syntax_step.meta.n_id, finding)


def _mark_methods(
    finding: core_model.FindingEnum,
    graph: graph_model.Graph,
    graph_syntax: graph_model.SyntaxSteps,
    methods: Set[str],
    marker: AppendLabelType,
) -> None:
    for syntax_steps in graph_syntax.values():
        for index, syntax_step in enumerate(syntax_steps):
            if isinstance(syntax_step, (
                graph_model.SyntaxStepMethodInvocation,
                graph_model.SyntaxStepMethodInvocationChain,
            )):
                method = syntax_step.method.rsplit('.', maxsplit=1)[-1]

                if (
                    method in methods or
                    syntax_step.method in methods
                ):
                    marker(graph, syntax_step.meta.n_id, finding)
                    continue

            if isinstance(syntax_step, (
                graph_model.SyntaxStepMethodInvocationChain,
            )):
                *_, parent = get_dependencies(index, syntax_steps)

                if isinstance(parent, graph_model.SyntaxStepMethodInvocation):
                    parent_method = parent.method.rsplit('.', maxsplit=1)[-1]
                    method = parent_method + '.' + method

                if method in methods:
                    marker(graph, syntax_step.meta.n_id, finding)


def _mark_methods_input(
    finding: core_model.FindingEnum,
    graph: graph_model.Graph,
    graph_syntax: graph_model.SyntaxSteps,
    methods: Set[str],
) -> None:
    _mark_methods(
        finding,
        graph,
        graph_syntax,
        methods,
        _append_label_input,
    )


def _mark_methods_sink(
    finding: core_model.FindingEnum,
    graph: graph_model.Graph,
    graph_syntax: graph_model.SyntaxSteps,
    methods: Set[str],
) -> None:
    _mark_methods(
        finding,
        graph,
        graph_syntax,
        methods,
        _append_label_sink,
    )


def _mark_obj_inst(
    finding: core_model.FindingEnum,
    graph: graph_model.Graph,
    graph_syntax: graph_model.SyntaxSteps,
    types: Set[str],
    marker: AppendLabelType,
) -> None:
    for syntax_steps in graph_syntax.values():
        for syntax_step in syntax_steps:
            if isinstance(syntax_step, (
                graph_model.SyntaxStepObjectInstantiation,
            )):
                if syntax_step.object_type in types:
                    marker(graph, syntax_step.meta.n_id, finding)


def _mark_obj_inst_input(
    finding: core_model.FindingEnum,
    graph: graph_model.Graph,
    graph_syntax: graph_model.SyntaxSteps,
    types: Set[str],
) -> None:
    _mark_obj_inst(
        finding,
        graph,
        graph_syntax,
        types,
        _append_label_input,
    )


def _mark_obj_inst_sink(
    finding: core_model.FindingEnum,
    graph: graph_model.Graph,
    graph_syntax: graph_model.SyntaxSteps,
    types: Set[str],
) -> None:
    _mark_obj_inst(
        finding,
        graph,
        graph_syntax,
        types,
        _append_label_sink,
    )


def mark(
    graph: graph_model.Graph,
    language: graph_model.GraphShardMetadataLanguage,
    syntax: graph_model.GraphSyntax,
) -> None:
    if language == graph_model.GraphShardMetadataLanguage.JAVA:
        _mark_java_inputs(graph, syntax)
        _mark_java_sinks(graph, syntax)
