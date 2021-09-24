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
    node_to_str,
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
            namespace = node_to_str(graph, match["__1__"])
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
                graph, c_id, "modifiers", "class", "identifier", "base_list"
            )
            class_identifier_id = match["identifier"]
            if not class_identifier_id:
                raise NotImplementedError()

            base_type_name = None
            if _base_list := match["base_list"]:
                _match_base = g.match_ast(graph, _base_list, "__0__", "__1__")
                base_type_name = node_to_str(graph, _match_base["__1__"])

            name = graph.nodes[class_identifier_id]["label_text"]
            qualified = namespace + "." + name
            classes[qualified] = graph_model.GraphShardMetadataClass(
                n_id=c_id,
                fields=_get_metadata_class_fields(graph, c_id),
                methods=_get_metadata_class_methods(graph, c_id),
                attributes=_get_metadata_class_attributes(graph, c_id),
                inherit=base_type_name,
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


def _get_method_return_type(
    graph: graph_model.Graph,
    method_declaration_id: str,
) -> Optional[str]:
    match_method = g.match_ast_group(
        graph,
        method_declaration_id,
        "identifier",
        "qualified_name",
        "predefined_type",
        "void_keyword",
    )
    # pylint: disable=used-before-assignment
    if (_identifiers := match_method["identifier"]) and len(_identifiers) == 2:
        return node_to_str(graph, _identifiers[0])
    if _qualified_name := match_method["qualified_name"]:
        return node_to_str(graph, _qualified_name[0])
    if _predefined_type := match_method["predefined_type"]:
        return node_to_str(graph, _predefined_type[0])
    if _void_keyword := match_method["void_keyword"]:
        return node_to_str(graph, _void_keyword[0])
    return None


def _get_method_name(
    graph: graph_model.Graph,
    method_declaration_id: str,
) -> str:
    match_method = g.match_ast_group(
        graph,
        method_declaration_id,
        "identifier",
    )
    _identifiers = match_method["identifier"]
    if len(_identifiers) == 2:
        return graph.nodes[_identifiers[1]]["label_text"]
    return graph.nodes[_identifiers[0]]["label_text"]


def _get_metadata_attributes(
    graph: graph_model.Graph,
    declaration_id: str,
) -> List[str]:
    attributes = list()
    attributes_match = g.match_ast_group(
        graph,
        declaration_id,
        "attribute_list",
    )
    for attribute_list in attributes_match["attribute_list"]:
        match_attribute = g.match_ast_group(graph, attribute_list, "attribute")
        for attribute in match_attribute["attribute"]:
            match = g.match_ast(graph, attribute, "__0__")
            name = node_to_str(graph, match["__0__"])
            attributes.append(name)
    return attributes


def _get_metadata_class_methods(
    graph: graph_model.Graph,
    n_id: str,
) -> Dict[str, graph_model.GraphShardMetadataClassField]:
    methods: Dict[str, graph_model.GraphShardMetadataCSharpMethod] = {}

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
                graph,
                method_id,
                "identifier",
                "modifier",
                "parameter_list",
                "qualified_name",
                "predefined_type",
                "void_keyword",
                "attribute_list",
            )
            _name = _get_method_name(graph, method_id)
            _parameters = {
                param.name: param
                for param in _get_metadata_method_parameters(
                    graph,
                    match_method["parameter_list"][0],
                )
            }
            is_static = any(
                g.match_ast(graph, modifier, "static")["static"]
                for modifier in match_method["modifier"] or list()
            )

            methods["." + _name] = graph_model.GraphShardMetadataCSharpMethod(
                method_id,
                class_name,
                name=_name,
                static=is_static,
                parameters=_parameters,
                attributes=_get_metadata_attributes(graph, method_id),
                return_type=_get_method_return_type(graph, method_id),
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
                name=name,
                parameters={
                    param.name: param
                    for param in _get_metadata_method_parameters(
                        graph,
                        graph.nodes[method_id]["label_field_parameters"],
                    )
                },
                attributes=_get_metadata_attributes(graph, method_id),
            )

    return methods


def _get_metadata_class_attributes(
    graph: graph_model.Graph,
    n_id: str,
) -> List[str]:
    attributes = list()
    attributes_match = g.match_ast_group(
        graph,
        n_id,
        "attribute_list",
    )
    for attribute_list in attributes_match["attribute_list"]:
        match_attribute = g.match_ast_group(graph, attribute_list, "attribute")
        for attribute in match_attribute["attribute"]:
            match = g.match_ast(graph, attribute, "__0__")
            name = node_to_str(graph, match["__0__"])
            attributes.append(name)  #
    return attributes


def _get_metadata_method_parameters(
    graph: graph_model.Graph,
    n_id: str,
) -> List[graph_model.GraphShardMetadataCSharpParameter]:
    parameters = list()
    match = g.match_ast_group(
        graph,
        n_id,
        "parameter",
    )
    for param_id in match.get("parameter") or list():
        match_param = g.match_ast(
            graph,
            param_id,
            "__0__",
            "__1__",
            "attribute_list",
        )
        if (
            len(match_param) >= 2
            and (_param_type_id := match_param["__0__"])
            and (_param_name_id := match_param["__1__"])
        ):
            _param_type = node_to_str(graph, _param_type_id)
            _param_name = graph.nodes[_param_name_id]["label_text"]
            parameters.append(
                graph_model.GraphShardMetadataCSharpParameter(
                    param_id,
                    name=_param_name,
                    type_name=_param_type,
                    attributes=_get_metadata_attributes(graph, param_id),
                )
            )
    return parameters
