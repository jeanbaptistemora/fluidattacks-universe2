from model import (
    core_model,
    graph_model,
)
from sast_transformations.danger_nodes.utils import (
    _append_label_input,
    mark_function_arg,
    mark_methods_sink,
)
from utils.string import (
    build_attr_paths,
)


def mark_inputs(
    graph: graph_model.Graph,
    syntax: graph_model.GraphSyntax,
) -> None:
    for finding in (core_model.FindingEnum.F063_TRUSTBOUND,):
        danger_args = {
            *build_attr_paths("*http", "Request"),
        }
        mark_function_arg(finding, graph, syntax, danger_args)

    for syntax_steps in syntax.values():
        for syntax_step in syntax_steps:
            if isinstance(syntax_step, graph_model.SyntaxStepLiteral) and (
                syntax_step.value_type == "struct[connect2V2.PSETransaction]"
            ):
                _append_label_input(
                    graph,
                    syntax_step.meta.n_id,
                    core_model.FindingEnum.F063_TYPE_CONFUSION,
                )


def mark_sinks(
    graph: graph_model.Graph,
    syntax: graph_model.GraphSyntax,
) -> None:
    findings = core_model.FindingEnum

    mark_methods_sink(
        findings.F063_TRUSTBOUND,
        graph,
        syntax,
        {
            "Exec",
            "ExecContext",
            "Query",
            "QueryContext",
            "QueryRow",
            "QueryRowContext",
        },
    )
