from model import (
    core_model,
    graph_model,
)
from sast_transformations.danger_nodes.utils import (
    mark_assignments_sink,
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
    mark_obj_inst_input(
        findings.F320,
        graph,
        syntax,
        {
            *build_attr_paths("System", "DirectoryServices", "DirectoryEntry"),
        },
    )


def mark_sinks(
    graph: graph_model.Graph,
    syntax: graph_model.GraphSyntax,
) -> None:
    findings = core_model.FindingEnum
    mark_assignments_sink(findings.F320, graph, syntax, {"AuthenticationType"})
