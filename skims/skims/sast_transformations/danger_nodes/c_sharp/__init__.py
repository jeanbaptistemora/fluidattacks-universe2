from model import (
    core_model,
    graph_model,
)
from sast_transformations.danger_nodes.c_sharp.web_api import (
    mark_metadata as mark_metadata_web_api,
)
from sast_transformations.danger_nodes.utils import (
    mark_assignments_sink,
    mark_function_arg,
    mark_methods_input,
    mark_methods_sink,
    mark_obj_inst_input,
)
from utils.string import (
    build_attr_paths,
)


def mark_inputs(
    graph: graph_model.Graph,
    syntax: graph_model.GraphSyntax,
) -> None:
    findings = core_model.FindingEnum

    for finding in (
        findings.F001_C_SHARP_SQL,
        findings.F004,
        findings.F008,
        findings.F021,
        findings.F063_PATH_TRAVERSAL,
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
    for finding in (
        findings.F004,
        findings.F021,
        findings.F063_PATH_TRAVERSAL,
        findings.F107,
    ):
        mark_obj_inst_input(
            finding,
            graph,
            syntax,
            {
                *build_attr_paths("System", "Net", "Sockets", "TcpClient"),
                *build_attr_paths("System", "Net", "Sockets", "TcpListener"),
                *build_attr_paths("System", "Data", "SqlClient", "SqlCommand"),
                *build_attr_paths("System", "IO", "StreamReader"),
                *build_attr_paths("System", "Net", "WebClient"),
            },
        )
    for finding in {
        findings.F004,
        findings.F021,
        findings.F063_PATH_TRAVERSAL,
        findings.F107,
    }:
        mark_methods_input(
            finding,
            graph,
            syntax,
            {
                "GetEnvironmentVariable",
            },
        )


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
    mark_methods_sink(
        findings.F004,
        graph,
        syntax,
        {
            "Start",
        },
    )
    mark_methods_sink(
        findings.F008,
        graph,
        syntax,
        {
            "Write",
        },
    )
    mark_assignments_sink(
        findings.F008,
        graph,
        syntax,
        {
            "StatusDescription",
        },
    )
    mark_methods_sink(
        findings.F021,
        graph,
        syntax,
        {
            "Evaluate",
        },
    )
    mark_methods_sink(
        findings.F063_PATH_TRAVERSAL,
        graph,
        syntax,
        {
            "Exists",
        },
    )


def mark_metadata(
    graph: graph_model.Graph,
    metadata: graph_model.GraphShardMetadata,
) -> None:
    mark_metadata_web_api(graph, metadata)
