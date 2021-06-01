from model import (
    graph_model,
)
from sast.inspectors.c_sharp import (
    get_metadata as get_metadata_c_sharp,
)
from sast.inspectors.java import (
    get_metadata as get_metadata_java,
)


def get_metadata(
    graph: graph_model.Graph,
    language: graph_model.GraphShardMetadataLanguage,
) -> graph_model.GraphShardMetadata:
    return graph_model.GraphShardMetadata(
        java=get_metadata_java(graph, language),
        c_sharp=get_metadata_c_sharp(graph, language),
        language=language,
    )
