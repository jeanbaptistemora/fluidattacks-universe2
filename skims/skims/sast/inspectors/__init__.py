# Standard library

# Local libraries
from model import (
    graph_model,
)

from sast.inspectors.java import get_metadata as get_metadata_java


def get_metadata(
    graph: graph_model.Graph,
    language: graph_model.GraphShardMetadataLanguage,
) -> graph_model.GraphShardMetadata:
    return graph_model.GraphShardMetadata(
        java=get_metadata_java(graph, language),
        language=language,
    )
