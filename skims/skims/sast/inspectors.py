# Standard library
from typing import (
    Dict,
)

# Local libraries
from utils import (
    graph as g,
)
from model import (
    graph_model,
)


def get_metadata(
    graph: graph_model.Graph,
    language: graph_model.GraphShardMetadataLanguage,
) -> graph_model.GraphShardMetadata:
    return graph_model.GraphShardMetadata(
        java=get_metadata_java(graph, language),
        language=language,
    )


def get_metadata_java(
    graph: graph_model.Graph,
    language: graph_model.GraphShardMetadataLanguage,
) -> graph_model.GraphShardMetadataJava:
    if language != graph_model.GraphShardMetadataLanguage.JAVA:
        return graph_model.GraphShardMetadataJava(
            classes={},
            package='',
        )

    classes = get_metadata_java_classes(graph)
    package = get_metadata_java_package(graph)

    classes_and_package = dict(())
    for key, item in classes.items():
        classes_and_package[package + key] = item
        if len(key.split('.')) > 2:
            key = key.split('.')[-1]
            classes_and_package[key] = item
            classes_and_package[f'.{key}'] = item
    classes.update(classes_and_package)
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
                    fields=get_metadata_java_class_fields(graph, c_id),
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


def get_metadata_java_class_fields(
    graph: graph_model.Graph,
    n_id: str,
) -> Dict[str, graph_model.GraphShardMetadataJavaClassField]:
    methods: Dict[str, graph_model.GraphShardMetadataJavaClassField] = {}

    if class_body_id := g.match_ast_d(graph, n_id, 'class_body'):
        for c_id in g.adj(graph, class_body_id):
            if not graph.nodes[c_id]['label_type'] == 'field_declaration':
                continue

            match = g.match_ast(
                graph, c_id,
                'modifiers', '__0__', 'variable_declarator', ';',
            )
            match_static = g.match_ast(graph, match['modifiers'], 'static')
            if (
                (type_id := match['__0__'])
                and (dcl_id := match['variable_declarator'])
                and (id_id := g.match_ast_d(graph, dcl_id, '__0__'))
            ):
                name = '.' + graph.nodes[id_id]['label_text']
                methods[name] = graph_model.GraphShardMetadataJavaClassField(
                    n_id=id_id,
                    var=graph.nodes[id_id]['label_text'],
                    var_type=graph.nodes[type_id]['label_text'],
                    static=bool(match_static['static'])
                )

    return methods


def get_metadata_java_class_methods(
    graph: graph_model.Graph,
    n_id: str,
) -> Dict[str, graph_model.GraphShardMetadataJavaClassField]:
    methods: Dict[str, graph_model.GraphShardMetadataJavaClassMethod] = {}

    match = g.match_ast(graph, n_id, 'class_body')
    class_name = '.' + graph.nodes[graph.nodes[n_id]
                                   ['label_field_name']]['label_text']

    if class_body_id := match['class_body']:
        for c_id in g.adj(graph, class_body_id):

            if graph.nodes[c_id]['label_type'] == 'method_declaration':
                match = g.match_ast(graph, c_id, 'identifier', 'modifiers')

                if identifier_id := match['identifier']:
                    name = '.' + graph.nodes[identifier_id]['label_text']
                    match_static = g.match_ast(
                        graph,
                        match['modifiers'],
                        'static',
                    )
                    methods[name] = \
                        graph_model.GraphShardMetadataJavaClassMethod(
                            c_id,
                            class_name,
                            static=bool(match_static['static'])
                    )
            elif graph.nodes[c_id]['label_type'] == 'constructor_declaration':
                identifier_id = graph.nodes[c_id]['label_field_name']
                p_id = graph.nodes[c_id]['label_field_parameters']
                params = g.match_ast_group(graph, p_id, 'formal_parameter')
                if not params['formal_parameter']:
                    params_length = 0
                else:
                    params_length = len(params['formal_parameter'])
                constructor = graph.nodes[identifier_id]["label_text"]
                name = f'.{constructor}_{params_length}'
                methods[name] = graph_model.GraphShardMetadataJavaClassMethod(
                    c_id,
                    class_name,
                )

    return methods
