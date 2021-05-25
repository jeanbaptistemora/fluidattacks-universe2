# Standard library
from typing import (
    Dict,
)

# Local libraries
from utils import (
    graph as g,
)
from utils.graph.transformation import build_qualified_name
from model import (
    graph_model,
)


def get_metadata(
    graph: graph_model.Graph,
    language: graph_model.GraphShardMetadataLanguage,
) -> graph_model.GraphShardMetadataCSharp:
    if language != graph_model.GraphShardMetadataLanguage.CSHARP:
        return graph_model.GraphShardMetadataCSharp(
            classes={},
            package="",
        )

    classes = _get_metadata_classes(graph)
    package = _get_metadata_package(graph)

    classes_and_package = dict(())
    for key, item in classes.items():
        classes_and_package[package + key] = item
        if len(key.split(".")) > 2:
            key = key.split(".")[-1]
            classes_and_package[key] = item
            classes_and_package[f".{key}"] = item
    classes.update(classes_and_package)
    return graph_model.GraphShardMetadataJava(
        classes=classes,
        package=package,
    )


def _get_metadata_package(graph: graph_model.Graph) -> str:
    match = g.match_ast(graph, g.ROOT_NODE, "namespace_declaration")
    namespace = ""
    if namespace_declaration := match["namespace_declaration"]:
        match = g.match_ast(
            graph,
            namespace_declaration,
            "__1__",
        )
        namespace_identifier_type = graph.nodes[match["__1__"]]["label_type"]
        if namespace_identifier_type == "identifier":
            namespace = graph.nodes[match["__1__"]]["label_text"]
        elif namespace_identifier_type == "qualified_name":
            namespace = build_qualified_name(graph, match["__1__"])
    return namespace


def _get_metadata_classes(
    graph: graph_model.Graph,
    n_id: str = g.ROOT_NODE,
    namespace: str = "",
) -> Dict[str, graph_model.GraphShardMetadataJavaClass]:
    classes: Dict[str, graph_model.GraphShardMetadataJavaClass] = {}

    for c_id in g.adj_ast(graph, n_id):
        if graph.nodes[c_id]["label_type"] == "class_declaration":
            match = g.match_ast(
                graph, c_id, "modifiers", "class", "identifier"
            )
            class_identifier_id = match["identifier"]
            if not class_identifier_id:
                raise NotImplementedError()

            name = graph.nodes[class_identifier_id]["label_text"]
            qualified = namespace + "." + name
            classes[qualified] = graph_model.GraphShardMetadataJavaClass(
                n_id=c_id,
                fields={},
                methods=_get_metadata_class_methods(graph, c_id),
            )

            # Recurse to get the class members
            classes.update(
                _get_metadata_classes(
                    graph,
                    c_id,
                    qualified,
                )
            )
        else:
            # Recurse to get the class members
            classes.update(
                _get_metadata_classes(
                    graph,
                    c_id,
                    namespace,
                )
            )

    return classes


def _get_metadata_class_methods(
    graph: graph_model.Graph,
    n_id: str,
) -> Dict[str, graph_model.GraphShardMetadataJavaClassField]:
    methods: Dict[str, graph_model.GraphShardMetadataJavaClassMethod] = {}

    class_body_id = g.match_ast(graph, n_id, "declaration_list")[
        "declaration_list"
    ]
    if not class_body_id:
        return methods
    class_name = (
        "." + graph.nodes[graph.nodes[n_id]["label_field_name"]]["label_text"]
    )

    for method_id in g.adj(graph, class_body_id):
        if graph.nodes[method_id]["label_type"] == "method_declaration":
            match_method = g.match_ast_group(
                graph, method_id, "identifier", "modifier"
            )

            if _identifiers := match_method["identifier"]:
                # pylint: disable=unsubscriptable-object
                name = "." + graph.nodes[_identifiers[0]]["label_text"]
                is_static = any(
                    g.match_ast(graph, modifier, "static")["static"]
                    for modifier in match_method["modifier"] or list()
                )
                methods[name] = graph_model.GraphShardMetadataJavaClassMethod(
                    method_id,
                    class_name,
                    static=is_static,
                )
        elif graph.nodes[method_id]["label_type"] == "constructor_declaration":
            params = g.match_ast_group(
                graph,
                graph.nodes[method_id]["label_field_parameters"],
                "parameter",
            )
            if not params["parameter"]:
                params_length = 0
            else:
                params_length = len(params["parameter"])
            constructor = graph.nodes[
                graph.nodes[method_id]["label_field_name"]
            ]["label_text"]
            name = f".{constructor}_{params_length}"
            methods[name] = graph_model.GraphShardMetadataJavaClassMethod(
                method_id,
                class_name,
            )

    return methods
