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


def get_metadata(
    graph: graph_model.Graph,
    language: graph_model.GraphShardMetadataLanguage,
) -> graph_model.GraphShardMetadataJava:
    if language != graph_model.GraphShardMetadataLanguage.JAVA:
        return graph_model.GraphShardMetadataJava(
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
    package: str = ""

    match = g.match_ast(graph, g.ROOT_NODE, "package_declaration")

    if n_id := match["package_declaration"]:
        match = g.match_ast(graph, n_id, "identifier", "scoped_identifier")

        if n_id := match["identifier"]:
            package = graph.nodes[n_id]["label_text"]
        elif n_id := match["scoped_identifier"]:
            # Exception: FP(There is an assignment in conditional)
            package = graph.nodes[n_id]["label_text"]  # NOSONAR

    return package


def _get_class_inherit(
    graph: graph_model.Graph,
    class_declaration_id: str,
) -> Optional[str]:
    match = g.match_ast(
        graph,
        class_declaration_id,
        "superclass",
    )
    if superclass := match["superclass"]:
        match_superclass = g.match_ast(
            graph,
            superclass,
            "extends",
            "__0__",
        )
        return graph.nodes[match_superclass["__0__"]].get("label_text")

    return None


def _get_metadata_classes(
    graph: graph_model.Graph,
    n_id: str = g.ROOT_NODE,
    namespace: str = "",
) -> Dict[str, graph_model.GraphShardMetadataClass]:
    classes: Dict[str, graph_model.GraphShardMetadataClass] = {}

    for c_id in g.adj_ast(graph, n_id):
        if graph.nodes[c_id]["label_type"] == "class_declaration":
            match = g.match_ast(
                graph,
                c_id,
                "modifiers",
                "class",
                "__0__",
            )

            if class_identifier_id := match["__0__"]:
                name = graph.nodes[class_identifier_id]["label_text"]
                qualified = namespace + "." + name
                classes[qualified] = graph_model.GraphShardMetadataClass(
                    n_id=c_id,
                    fields=_get_metadata_class_fields(graph, c_id),
                    methods=_get_metadata_class_methods(graph, c_id),
                    inherit=_get_class_inherit(graph, c_id),
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
                raise NotImplementedError()
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


def _get_metadata_class_fields(
    graph: graph_model.Graph,
    n_id: str,
) -> Dict[str, graph_model.GraphShardMetadataClassField]:
    methods: Dict[str, graph_model.GraphShardMetadataClassField] = {}

    if class_body_id := g.match_ast_d(graph, n_id, "class_body"):
        for c_id in g.adj(graph, class_body_id):
            if not graph.nodes[c_id]["label_type"] == "field_declaration":
                continue

            match = g.match_ast(
                graph,
                c_id,
                "modifiers",
                "__0__",
                "variable_declarator",
                ";",
            )
            match_static = g.match_ast(graph, match["modifiers"], "static")
            if (
                (type_id := match["__0__"])
                and (dcl_id := match["variable_declarator"])
                and (id_id := g.match_ast_d(graph, dcl_id, "__0__"))
            ):
                name = "." + graph.nodes[id_id]["label_text"]
                methods[name] = graph_model.GraphShardMetadataClassField(
                    n_id=id_id,
                    var=graph.nodes[id_id]["label_text"],
                    var_type=graph.nodes[type_id]["label_text"],
                    static=bool(match_static["static"]),
                )

    return methods


def _get_metadata_method_parameters(
    graph: graph_model.Graph,
    formal_parameters_id: str,
) -> List[graph_model.GraphShardMetadataParameter]:
    parameters = list()
    match = g.match_ast_group(graph, formal_parameters_id, "formal_parameter")
    for _parameter in match["formal_parameter"] or list():
        match_parameter = g.match_ast(
            graph, _parameter, "__0__", "__1__", "modifiers"
        )
        type_name = graph.nodes[match_parameter["__0__"]]["label_text"]
        name = graph.nodes[match_parameter["__1__"]]["label_text"]
        parameters.append(
            graph_model.GraphShardMetadataParameter(
                _parameter,
                name=name,
                type_name=type_name,
            )
        )
    return parameters


def _get_metadata_class_methods(
    graph: graph_model.Graph,
    n_id: str,
) -> Dict[str, graph_model.GraphShardMetadataClassField]:
    methods: Dict[str, graph_model.GraphShardMetadataClassMethod] = {}

    match = g.match_ast(graph, n_id, "class_body")
    class_name = (
        "." + graph.nodes[graph.nodes[n_id]["label_field_name"]]["label_text"]
    )

    if class_body_id := match["class_body"]:
        for c_id in g.adj(graph, class_body_id):

            if graph.nodes[c_id]["label_type"] == "method_declaration":
                match = g.match_ast(
                    graph,
                    c_id,
                    "identifier",
                    "modifiers",
                    "formal_parameters",
                )

                _name = graph.nodes[match["identifier"]]["label_text"]
                static = False
                if match["modifiers"]:
                    match_static = g.match_ast(
                        graph,
                        match["modifiers"],
                        "static",
                    )
                    static = bool(match_static["static"])
                methods[
                    "." + _name
                ] = graph_model.GraphShardMetadataClassMethod(
                    c_id,
                    class_name,
                    name=_name,
                    static=static,
                    parameters={
                        param.name: param
                        for param in _get_metadata_method_parameters(
                            graph,
                            match["formal_parameters"],
                        )
                    },
                )
            elif graph.nodes[c_id]["label_type"] == "constructor_declaration":
                p_id = graph.nodes[c_id]["label_field_parameters"]
                params = g.match_ast_group(graph, p_id, "formal_parameter")
                if not params["formal_parameter"]:
                    params_length = 0
                else:
                    params_length = len(params["formal_parameter"])
                constructor = graph.nodes[
                    graph.nodes[c_id]["label_field_name"]
                ]["label_text"]
                name = f".{constructor}_{params_length}"
                methods[name] = graph_model.GraphShardMetadataClassMethod(
                    c_id,
                    class_name,
                    parameters={
                        param.name: param
                        for param in _get_metadata_method_parameters(
                            graph,
                            p_id,
                        )
                    },
                )

    return methods
