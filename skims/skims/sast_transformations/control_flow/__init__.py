# Local Imports
from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage,
)
from sast_transformations.control_flow.java import add as java_add
from sast_transformations.control_flow.c_sharp import add as c_sharp_add


def add(
    graph: Graph,
    language: GraphShardMetadataLanguage,
) -> None:
    if language == GraphShardMetadataLanguage.JAVA:
        java_add(graph)
    elif language == GraphShardMetadataLanguage.CSHARP:
        c_sharp_add(graph)
