from model import (
    graph_model,
)
from typing import (
    Dict,
    List,
    Optional,
)
from utils import (
    graph as g,
)
from utils.graph.transformation import (
    build_qualified_name,
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
    return graph_model.GraphShardMetadataCSharp(
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
) -> Dict[str, graph_model.GraphShardMetadataClass]:
    classes: Dict[str, graph_model.GraphShardMetadataClass] = {}

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
            classes[qualified] = graph_model.GraphShardMetadataClass(
                n_id=c_id,
                fields=_get_metadata_class_fields(graph, c_id),
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


def _get_assignment_value(
    graph: graph_model.Graph, var_declarators: List[str]
) -> Optional[str]:
    # it can be a multiple assignment, only the last assignment has the value
    for var_declarator in var_declarators or set():
        match_declarator = g.match_ast(
            graph,
            var_declarator,
            "identifier",
            "equals_value_clause",
        )
        if equals := match_declarator["equals_value_clause"]:
            match_equals = g.match_ast(
                graph,
                equals,
                "=",
                "__0__",
            )
            if id_id := match_equals["__0__"]:
                return id_id
    return None


def _get_metadata_class_fields(
    graph: graph_model.Graph,
    n_id: str,
) -> Dict[str, graph_model.GraphShardMetadataClassField]:
    methods: Dict[str, graph_model.GraphShardMetadataClassField] = {}
    class_body_id = g.match_ast_d(graph, n_id, "declaration_list")
    if not class_body_id:
        return methods
    for field_id in (
        g.match_ast_group(graph, class_body_id, "field_declaration")[
            "field_declaration"
        ]
        or list()
    ):
        match_field = g.match_ast(
            graph,
            field_id,
            "modifier",
            "__0__",
            "variable_declaration",
        )
        is_static = any(
            g.match_ast(graph, modifier, "static")["static"]
            for modifier in g.match_ast_group(graph, field_id, "modifier")[
                "modifier"
            ]
            or list()
        )

        match_declaration = g.match_ast_group(
            graph,
            match_field["variable_declaration"],
            "variable_declarator",
            "__0__",
        )
        if not match_declaration["variable_declarator"]:
            continue

        var_type_id = match_declaration["__0__"]
        assignment_value = _get_assignment_value(
            graph, match_declaration["variable_declarator"]
        )
        for var_declarator in (
            match_declaration["variable_declarator"] or set()
        ):
            match_declarator = g.match_ast(
                graph,
                var_declarator,
                "identifier",
            )
            var_identifier = match_declarator["identifier"]

            if assignment_value and (
                var_type := graph.nodes[var_type_id].get("label_text")
            ):
                name = "." + graph.nodes[var_identifier]["label_text"]
                methods[name] = graph_model.GraphShardMetadataClassField(
                    n_id=assignment_value,
                    var=graph.nodes[var_identifier]["label_text"],
                    var_type=var_type,
                    static=is_static,
                )

    return methods


def _get_metadata_class_methods(
    graph: graph_model.Graph,
    n_id: str,
) -> Dict[str, graph_model.GraphShardMetadataClassField]:
    methods: Dict[str, graph_model.GraphShardMetadataClassMethod] = {}

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
                name = "." + graph.nodes[_identifiers[0]]["label_text"]
                is_static = any(
                    g.match_ast(graph, modifier, "static")["static"]
                    for modifier in match_method["modifier"] or list()
                )
                methods[name] = graph_model.GraphShardMetadataClassMethod(
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
            methods[name] = graph_model.GraphShardMetadataClassMethod(
                method_id,
                class_name,
            )

    return methods
