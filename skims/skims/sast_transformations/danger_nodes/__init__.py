from model import (
    graph_model,
)
from sast_transformations.danger_nodes.c_sharp import (
    mark_inputs as c_sharp_mark_inputs,
    mark_sinks as c_sharp_mark_sinks,
)
from sast_transformations.danger_nodes.java import (
    mark_inputs as java_mark_inputs,
    mark_sinks as java_mark_sinks,
)


def mark(
    graph: graph_model.Graph,
    language: graph_model.GraphShardMetadataLanguage,
    syntax: graph_model.GraphSyntax,
) -> None:
    if language == graph_model.GraphShardMetadataLanguage.JAVA:
        java_mark_inputs(graph, syntax)
        java_mark_sinks(graph, syntax)
    elif language == graph_model.GraphShardMetadataLanguage.CSHARP:
        c_sharp_mark_inputs(graph, syntax)
        c_sharp_mark_sinks(graph, syntax)
