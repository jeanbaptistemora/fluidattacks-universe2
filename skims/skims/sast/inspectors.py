# Standard library
from typing import (
    Any,
    Dict,
    Optional,
)

# Local libraries
from utils import (
    graph as g,
)
from model.graph_model import (
    Graph,
    GraphShardMetadata,
    GraphShardMetadataJava,
    GraphShardMetadataJavaClass,
    GraphShardMetadataJavaClassMethod,
    GraphShardMetadataLanguage,
)


def get_metadata(
    graph: Graph,
    language: GraphShardMetadataLanguage,
) -> GraphShardMetadata:

    metadata: Dict[str, Optional[Any]] = {
        'java': None,
    }

    if language == GraphShardMetadataLanguage.JAVA:
        metadata['java'] = get_metadata_java(graph)
    else:
        raise NotImplementedError()

    return GraphShardMetadata(language=language, **metadata)


def get_metadata_java(graph: Graph) -> GraphShardMetadataJava:
    classes = get_metadata_java_classes(graph)
    package = get_metadata_java_package(graph)

    return GraphShardMetadataJava(
        classes=classes,
        package=package,
    )


def get_metadata_java_package(graph: Graph) -> str:
    package: str = ''

    match = g.match_ast(graph, g.ROOT_NODE, 'package_declaration')

    if n_id := match['package_declaration']:
        match = g.match_ast(graph, n_id, 'identifier', 'scoped_identifier')

        if n_id := match['identifier']:
            package = graph.nodes[n_id]['label_text']
        elif n_id := match['scoped_identifier']:
            package = graph.nodes[n_id]['label_text']

    return package


def get_metadata_java_classes(
    graph: Graph,
    n_id: str = g.ROOT_NODE,
    namespace: str = '',
) -> Dict[str, GraphShardMetadataJavaClass]:
    classes: Dict[str, GraphShardMetadataJavaClass] = {}

    for c_id in g.adj_ast(graph, n_id):
        if graph.nodes[c_id]['label_type'] == 'class_declaration':
            match = g.match_ast(graph, c_id, 'modifiers', 'class', '__0__')

            if class_identifier_id := match['__0__']:
                name = graph.nodes[class_identifier_id]['label_text']
                name_qualified = namespace + '.' + name
                classes[name_qualified] = GraphShardMetadataJavaClass(
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
    graph: Graph,
    n_id: str,
) -> Dict[str, GraphShardMetadataJavaClassMethod]:
    methods: Dict[str, GraphShardMetadataJavaClassMethod] = {}

    match = g.match_ast(graph, n_id, 'class_body')

    if class_body_id := match['class_body']:
        for c_id in g.adj(graph, class_body_id):

            if graph.nodes[c_id]['label_type'] == 'method_declaration':
                match = g.match_ast(graph, c_id, 'identifier')

                if identifier_id := match['identifier']:
                    name = graph.nodes[identifier_id]['label_text']
                    methods[name] = GraphShardMetadataJavaClassMethod(
                        n_id=c_id,
                    )

    return methods
