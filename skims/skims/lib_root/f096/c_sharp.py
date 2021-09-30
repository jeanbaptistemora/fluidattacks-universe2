from itertools import (
    chain,
)
from lib_root.utilities.c_sharp import (
    get_variable_attribute,
    yield_object_creation,
)
from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils.graph import (
    get_ast_childs,
    match_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


# https://docs.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-security-guide
def insecure_deserialization(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    danger_objects = {
        "BinaryFormatter",
        "SoapFormatter",
        "NetDataContractSerializer",
        "LosFormatter",
        "ObjectStateFormatter",
    }

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            for syntax_steps in shard.syntax.values():
                for syntax_step in syntax_steps:
                    if (
                        isinstance(
                            syntax_step,
                            graph_model.SyntaxStepObjectInstantiation,
                        )
                        and syntax_step.object_type in danger_objects
                    ):
                        yield shard, syntax_step.meta.n_id

    return get_vulnerabilities_from_n_ids(
        cwe=("502",),
        desc_key="F096.title",
        desc_params={},
        finding=core_model.FindingEnum.F096,
        graph_shard_nodes=n_ids(),
    )


def check_xml_serializer(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard, member in chain(
            yield_object_creation(graph_db, {"XmlSerializer"}),
        ):
            type_node = get_ast_childs(
                shard.graph, member, "argument", depth=2
            )
            type_var = match_ast(shard.graph, type_node[0])["__0__"]
            if (
                len(type_node) > 0
                and shard.graph.nodes[type_var].get("label_type")
                == "identifier"
            ):
                var_value = get_variable_attribute(
                    shard.graph,
                    shard.graph.nodes[type_var].get("label_text"),
                    "label_text",
                )
            elif (
                len(type_node) > 0
                and shard.graph.nodes[type_var].get("label_type")
                == "invocation_expression"
            ):
                var_value = node_to_str(shard.graph, type_var)
            if var_value:
                var_items = var_value.split("(")
                for _class in shard.metadata.c_sharp.classes.values():
                    for _method in _class.methods.values():
                        if (
                            var_items[0] == "Type.GetType"
                            and len(var_items) > 1
                            and var_items[1].replace(")", "")
                            in _method.parameters.keys()
                            and _method.parameters[
                                var_items[1].replace(")", "")
                            ].type_name
                            == "HttpRequest"
                        ):
                            yield shard, member

    return get_vulnerabilities_from_n_ids(
        cwe=("502",),
        desc_key="F096.title",
        desc_params={},
        finding=core_model.FindingEnum.F096,
        graph_shard_nodes=n_ids(),
    )
