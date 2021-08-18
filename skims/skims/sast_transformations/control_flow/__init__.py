from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage,
)
from sast_transformations.control_flow.c_sharp import (
    add as c_sharp_add,
)
from sast_transformations.control_flow.go import (
    add as go_add,
)
from sast_transformations.control_flow.java import (
    add as java_add,
)
from sast_transformations.control_flow.javascript import (
    add as javascript_add,
)
from sast_transformations.control_flow.kotlin import (
    add as kotlin_add,
)


def add(
    graph: Graph,
    language: GraphShardMetadataLanguage,
) -> None:
    if language == GraphShardMetadataLanguage.JAVA:
        java_add(graph)
    elif language == GraphShardMetadataLanguage.JAVASCRIPT:
        javascript_add(graph)
    elif language == GraphShardMetadataLanguage.CSHARP:
        c_sharp_add(graph)
    elif language == GraphShardMetadataLanguage.GO:
        go_add(graph)
    elif language == GraphShardMetadataLanguage.KOTLIN:
        kotlin_add(graph)
