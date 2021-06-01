from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage,
)
from sast_transformations.program_dependencie.c_sharp import (
    add as c_sharp_add,
)


def add(
    graph: Graph,
    language: GraphShardMetadataLanguage,
) -> None:
    if language == GraphShardMetadataLanguage.CSHARP:
        c_sharp_add(graph)
