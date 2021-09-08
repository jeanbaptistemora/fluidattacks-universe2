from model import (
    core_model,
    graph_model,
)
from more_itertools import (
    flatten,
)
from sast_syntax_readers.utils_generic import (
    get_dependencies,
)
from typing import (
    Callable,
    Set,
)
from utils.string import (
    split_on_last_dot,
)


def append_label(
    graph: graph_model.Graph,
    n_id: str,
    label: str,
    finding: core_model.FindingEnum,
) -> None:
    if label in graph.nodes[n_id]:
        graph.nodes[n_id][label].add(finding.name)
    else:
        graph.nodes[n_id][label] = {finding.name}


AppendLabelType = Callable[
    [graph_model.Graph, str, core_model.FindingEnum], None
]


def _append_label_input(
    graph: graph_model.Graph,
    n_id: str,
    finding: core_model.FindingEnum,
) -> None:
    append_label(graph, n_id, "label_input_type", finding)


def _append_label_sink(
    graph: graph_model.Graph,
    n_id: str,
    finding: core_model.FindingEnum,
) -> None:
    append_label(graph, n_id, "label_sink_type", finding)


def _mark_array(
    finding: core_model.FindingEnum,
    graph: graph_model.Graph,
    graph_syntax: graph_model.SyntaxSteps,
    types: Set[str],
    marker: AppendLabelType,
) -> None:
    for syntax_steps in graph_syntax.values():
        for syntax_step in syntax_steps:
            if isinstance(
                syntax_step, (graph_model.SyntaxStepArrayInstantiation,)
            ) and (syntax_step.array_type in types):
                marker(graph, syntax_step.meta.n_id, finding)


def mark_array_input(
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


def mark_function_arg(
    finding: core_model.FindingEnum,
    graph: graph_model.Graph,
    graph_syntax: graph_model.SyntaxSteps,
    dangerous_types: Set[str],
) -> None:
    for syntax_steps in graph_syntax.values():
        for syntax_step in syntax_steps:
            if isinstance(syntax_step, graph_model.SyntaxStepDeclaration) and (
                syntax_step.var_type in dangerous_types
                or (
                    syntax_step.modifiers
                    and syntax_step.modifiers.intersection(dangerous_types)
                )
            ):
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
            if isinstance(
                syntax_step,
                (
                    graph_model.SyntaxStepMethodInvocation,
                    graph_model.SyntaxStepMethodInvocationChain,
                ),
            ):
                method = syntax_step.method.rsplit(".", maxsplit=1)[-1]

                if method in methods or syntax_step.method in methods:
                    marker(graph, syntax_step.meta.n_id, finding)
                    continue

            if isinstance(
                syntax_step, (graph_model.SyntaxStepMethodInvocationChain,)
            ):
                *_, parent = get_dependencies(index, syntax_steps)

                if isinstance(parent, graph_model.SyntaxStepMethodInvocation):
                    parent_method = parent.method.rsplit(".", maxsplit=1)[-1]
                    method = parent_method + "." + method

                if method in methods:
                    marker(graph, syntax_step.meta.n_id, finding)


def _mark_assignments(
    finding: core_model.FindingEnum,
    graph: graph_model.Graph,
    graph_syntax: graph_model.SyntaxSteps,
    attributes: Set[str],
    marker: AppendLabelType,
) -> None:
    for syntax_step in flatten(
        syntax_steps for syntax_steps in graph_syntax.values()
    ):
        if isinstance(syntax_step, graph_model.SyntaxStepAssignment):
            _, field = split_on_last_dot(syntax_step.var)
            if field and field in attributes:
                marker(graph, syntax_step.meta.n_id, finding)


def mark_methods_input(
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


def mark_methods_sink(
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
            if (
                isinstance(
                    syntax_step, (graph_model.SyntaxStepObjectInstantiation,)
                )
                and syntax_step.object_type in types
            ):
                marker(graph, syntax_step.meta.n_id, finding)


def mark_obj_inst_input(
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


def mark_obj_inst_sink(
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


def mark_assignments_sink(
    finding: core_model.FindingEnum,
    graph: graph_model.Graph,
    graph_syntax: graph_model.SyntaxSteps,
    attributes: Set[str],
) -> None:
    _mark_assignments(
        finding,
        graph,
        graph_syntax,
        attributes,
        _append_label_sink,
    )
