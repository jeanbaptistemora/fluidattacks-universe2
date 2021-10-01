from model.core_model import (
    FindingEnum,
)
from model.graph_model import (
    Graph,
    GraphSyntax,
)
from sast_transformations.danger_nodes.javascript import (
    express,
)
from sast_transformations.danger_nodes.utils import (
    mark_methods_sink,
)


def mark_sinks(
    graph: Graph,
    syntax: GraphSyntax,
) -> None:
    mark_methods_sink(
        FindingEnum.F004,
        graph,
        syntax,
        {
            "exec",
        },
    )


def mark_inputs(
    graph: Graph,
    syntax: GraphSyntax,
) -> None:
    express.mark_requests(graph, syntax)
