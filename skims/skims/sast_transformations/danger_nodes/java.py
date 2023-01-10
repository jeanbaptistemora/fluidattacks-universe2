from model import (
    core_model,
    graph_model,
)
from sast_transformations.danger_nodes.utils import (
    mark_obj_inst_input,
    mark_obj_inst_sink,
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
        findings.F034,
        graph,
        syntax,
        {
            *build_attr_paths("java", "util", "Random"),
        },
    )


def mark_sinks(
    graph: graph_model.Graph,
    syntax: graph_model.GraphSyntax,
) -> None:
    findings = core_model.FindingEnum
    mark_obj_inst_sink(
        findings.F063,
        graph,
        syntax,
        {
            *build_attr_paths("java", "io", "File"),
            *build_attr_paths("java", "io", "FileInputStream"),
            *build_attr_paths("java", "io", "FileOutputStream"),
        },
    )
