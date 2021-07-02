from model import (
    core_model,
    graph_model,
)
from sast_transformations.danger_nodes.utils import (
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
    findings = core_model.FindingEnum

    for finding in (findings.F063_TRUSTBOUND,):
        danger_args = {
            *build_attr_paths("*http", "Request"),
        }
        mark_function_arg(finding, graph, syntax, danger_args)


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
