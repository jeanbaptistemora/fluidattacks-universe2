from model.graph_model import (
    Graph,
    GraphShardMetadata,
    GraphShardMetadataLanguage,
    GraphSyntax,
)
from sast_transformations.danger_nodes.c_sharp import (
    mark_inputs as c_sharp_mark_inputs,
    mark_metadata as mark_metadata_c_sharp,
    mark_sinks as c_sharp_mark_sinks,
)
from sast_transformations.danger_nodes.java import (
    mark_inputs as java_mark_inputs,
    mark_sinks as java_mark_sinks,
)
from sast_transformations.danger_nodes.javascript import (
    mark_inputs as javascript_mark_imputs,
    mark_sinks as javascript_mark_sinks,
)


def mark(
    graph: Graph,
    language: GraphShardMetadataLanguage,
    syntax: GraphSyntax,
) -> None:
    if language == GraphShardMetadataLanguage.JAVA:
        java_mark_inputs(graph, syntax)
        java_mark_sinks(graph, syntax)
    elif language == GraphShardMetadataLanguage.CSHARP:
        c_sharp_mark_inputs(graph, syntax)
        c_sharp_mark_sinks(graph, syntax)
    elif language == GraphShardMetadataLanguage.JAVASCRIPT:
        javascript_mark_imputs(graph, syntax)
        javascript_mark_sinks(graph, syntax)


def mark_metadata(
    graph: Graph,
    metadata: GraphShardMetadata,
    language: GraphShardMetadataLanguage,
) -> None:
    if language == GraphShardMetadataLanguage.CSHARP:
        mark_metadata_c_sharp(graph, metadata)
