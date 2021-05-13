# Local libraries
from model import graph_model
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
