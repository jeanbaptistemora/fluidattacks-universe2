from model import (
    graph_model,
    core_model,
)
from sast_transformations.danger_nodes.utils import (
    mark_function_arg,
    mark_methods_sink,
)
from utils.string import build_attr_paths


def mark_inputs(
    graph: graph_model.Graph,
    syntax: graph_model.GraphSyntax,
) -> None:
    findings = core_model.FindingEnum

    for finding in (
        findings.F001_C_SHARP_SQL,
        findings.F107,
    ):
        danger_args = {
            *build_attr_paths(
                "System",
                "Web",
                "HttpRequest",
            ),
        }
        mark_function_arg(finding, graph, syntax, danger_args)


def mark_sinks(
    graph: graph_model.Graph,
    syntax: graph_model.GraphSyntax,
) -> None:
    findings = core_model.FindingEnum

    mark_methods_sink(
        findings.F001_C_SHARP_SQL,
        graph,
        syntax,
        {
            "ExecuteNonQuery",
            "ExecuteScalar",
        },
    )
    mark_methods_sink(
        findings.F107,
        graph,
        syntax,
        {
            "FindOne",
        },
    )
