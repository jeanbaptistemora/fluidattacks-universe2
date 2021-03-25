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
from model import (
    core_model,
    graph_model,
)


def get_metadata(
    graph: graph_model.Graph,
    language: graph_model.GraphShardMetadataLanguage,
) -> graph_model.GraphShardMetadata:

    metadata: Dict[str, Optional[Any]] = {
        'java': None,
    }

    if language == graph_model.GraphShardMetadataLanguage.JAVA:
        metadata['java'] = get_metadata_java(graph)
    else:
        raise NotImplementedError()

    return graph_model.GraphShardMetadata(
        language=language,
        nodes=graph_model.GraphShardMetadataNodes(
            dangerous_action={
                finding.name: tuple(
                    n_id
                    for n_id in graph.nodes
                    for label in [graph.nodes[n_id].get('label_sink_type')]
                    if label
                    for _label in label.split(',')
                    if core_model.FINDING_ENUM_FROM_STR[_label] == finding
                )
                for finding in core_model.FindingEnum
            },
            in_cfg=tuple(
                n_id
                for n_id in graph.nodes
                if g.is_connected_to_cfg(graph, n_id)
            ),
            untrusted={
                finding.name: tuple(
                    n_id
                    for n_id in graph.nodes
                    for label in [graph.nodes[n_id].get('label_input_type')]
                    if label
                    and any(
                        core_model.FINDING_ENUM_FROM_STR.get(label_find) ==
                        finding
                        for label_find in label.split(',')
                    )
                )
                for finding in core_model.FindingEnum
            },
        ),
        **metadata,
    )


def get_metadata_java(
    graph: graph_model.Graph,
) -> graph_model.GraphShardMetadataJava:
    classes = get_metadata_java_classes(graph)
    package = get_metadata_java_package(graph)

    return graph_model.GraphShardMetadataJava(
        classes=classes,
        package=package,
    )


def get_metadata_java_package(graph: graph_model.Graph) -> str:
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
    graph: graph_model.Graph,
    n_id: str = g.ROOT_NODE,
    namespace: str = '',
) -> Dict[str, graph_model.GraphShardMetadataJavaClass]:
    classes: Dict[str, graph_model.GraphShardMetadataJavaClass] = {}

    for c_id in g.adj_ast(graph, n_id):
        if graph.nodes[c_id]['label_type'] == 'class_declaration':
            match = g.match_ast(graph, c_id, 'modifiers', 'class', '__0__')

            if class_identifier_id := match['__0__']:
                name = graph.nodes[class_identifier_id]['label_text']
                qualified = namespace + '.' + name
                classes[qualified] = graph_model.GraphShardMetadataJavaClass(
                    n_id=c_id,
                    methods=get_metadata_java_class_methods(graph, c_id),
                )

                # Recurse to get the class members
                classes.update(get_metadata_java_classes(
                    graph, c_id, qualified,
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
    graph: graph_model.Graph,
    n_id: str,
) -> Dict[str, graph_model.GraphShardMetadataJavaClassMethod]:
    methods: Dict[str, graph_model.GraphShardMetadataJavaClassMethod] = {}

    match = g.match_ast(graph, n_id, 'class_body')

    if class_body_id := match['class_body']:
        for c_id in g.adj(graph, class_body_id):

            if graph.nodes[c_id]['label_type'] == 'method_declaration':
                match = g.match_ast(graph, c_id, 'identifier')

                if identifier_id := match['identifier']:
                    name = '.' + graph.nodes[identifier_id]['label_text']
                    methods[name] = \
                        graph_model.GraphShardMetadataJavaClassMethod(c_id)

    return methods
