# Standard library
from typing import (
    Any,
    Dict,
    Optional,
)

# Third party libraries
import networkx as nx

# Local libraries
from utils import (
    graph as g,
)
from utils.model import (
    ParsedFileMetadata, ParsedFileMetadataJava,
)


def get_metadata(
    graph: nx.DiGraph,
    language: str,
) -> ParsedFileMetadata:

    metadata: Dict[str, Optional[Any]] = {
        'java': None,
    }

    if language == 'java':
        metadata['java'] = get_metadata_java(graph)
    else:
        raise NotImplementedError()

    return ParsedFileMetadata(**metadata)


def get_metadata_java(graph: nx.DiGraph) -> ParsedFileMetadataJava:
    package = get_metadata_java_package(graph)

    return ParsedFileMetadataJava(
        package=package,
    )


def get_metadata_java_package(graph: nx.DiGraph) -> str:
    package: str = ''

    match = g.match_ast(graph, '1', 'package_declaration')

    if n_id := match['package_declaration']:
        match = g.match_ast(graph, n_id, 'identifier', 'scoped_identifier')

        if n_id := match['identifier']:
            package = graph.nodes[n_id]['label_text']
        elif n_id := match['scoped_identifier']:
            package = graph.nodes[n_id]['label_text']

    return package
