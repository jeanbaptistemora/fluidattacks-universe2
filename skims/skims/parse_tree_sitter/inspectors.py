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
    ParsedFileMetadata,
    ParsedFileMetadataJava,
    ParsedFileMetadataJavaClass,
    ParsedFileMetadataJavaClassMethod,
)

# Constants
ROOT = '1'


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
    classes = get_metadata_java_classes(graph)
    package = get_metadata_java_package(graph)

    return ParsedFileMetadataJava(
        classes=classes,
        package=package,
    )


def get_metadata_java_package(graph: nx.DiGraph) -> str:
    package: str = ''

    match = g.match_ast(graph, ROOT, 'package_declaration')

    if n_id := match['package_declaration']:
        match = g.match_ast(graph, n_id, 'identifier', 'scoped_identifier')

        if n_id := match['identifier']:
            package = graph.nodes[n_id]['label_text']
        elif n_id := match['scoped_identifier']:
            package = graph.nodes[n_id]['label_text']

    return package


def get_metadata_java_classes(
    graph: nx.DiGraph,
    n_id: str = ROOT,
    namespace: str = '',
) -> Dict[str, ParsedFileMetadataJavaClass]:
    classes: Dict[str, ParsedFileMetadataJavaClass] = {}

    for c_id in g.adj_ast(graph, n_id):
        if graph.nodes[c_id]['label_type'] == 'class_declaration':
            match = g.match_ast(graph, c_id, 'modifiers', 'class', '__0__')

            if class_identifier_id := match['__0__']:
                name = graph.nodes[class_identifier_id]['label_text']
                name_qualified = namespace + '.' + name
                classes[name_qualified] = ParsedFileMetadataJavaClass(
                    n_id=c_id,
                    methods=get_metadata_java_class_methods(graph, c_id),
                )

                # Recurse to get the class members
                classes.update(get_metadata_java_classes(
                    graph, c_id, name_qualified,
                ))
            else:
                raise NotImplementedError()
        else:
            # Recurse to get the class members
            classes.update(get_metadata_java_classes(
                graph, c_id, namespace,
            ))

    return classes


def get_metadata_java_class_methods(
    graph: nx.DiGraph,
    n_id: str,
) -> Dict[str, ParsedFileMetadataJavaClassMethod]:
    methods: Dict[str, ParsedFileMetadataJavaClassMethod] = {}

    match = g.match_ast(graph, n_id, 'class_body')

    if class_body_id := match['class_body']:
        for c_id in g.adj(graph, class_body_id):

            if graph.nodes[c_id]['label_type'] == 'method_declaration':
                match = g.match_ast(graph, c_id, 'identifier')

                if identifier_id := match['identifier']:
                    name = graph.nodes[identifier_id]['label_text']
                    methods[name] = ParsedFileMetadataJavaClassMethod(
                        n_id=c_id,
                    )

    return methods
