from model import (
    graph_model,
)
from sast_transformations.danger_nodes.c_sharp import (
    mark_inputs as c_sharp_mark_inputs,
    mark_metadata as mark_metadata_c_sharp,
    mark_sinks as c_sharp_mark_sinks,
)
from sast_transformations.danger_nodes.go import (
    mark_inputs as go_mark_inputs,
    mark_sinks as go_mark_sinks,
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
    elif language == graph_model.GraphShardMetadataLanguage.GO:
        go_mark_inputs(graph, syntax)
        go_mark_sinks(graph, syntax)


def mark_metadata(
    graph: graph_model.Graph,
    metadata: graph_model.GraphShardMetadata,
    language: graph_model.GraphShardMetadataLanguage,
) -> None:
    if language == graph_model.GraphShardMetadataLanguage.CSHARP:
        mark_metadata_c_sharp(graph, metadata)
