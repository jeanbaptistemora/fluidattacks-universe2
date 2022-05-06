from lib_root.utilities.c_sharp import (
    get_variable_attribute,
    yield_shard_object_creation,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
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
    shard_db: ShardDb,  # pylint: disable=unused-argument
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
        desc_key="criteria.vulns.096.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=core_model.MethodsEnum.CS_INSECURE_DESERIAL,
    )


def check_xml_serializer(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    c_sharp = graph_model.GraphShardMetadataLanguage.CSHARP

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            for node in yield_shard_object_creation(shard, {"XmlSerializer"}):
                var_value = ""
                type_node = get_ast_childs(
                    shard.graph, node, "argument", depth=2
                )
                type_var = match_ast(shard.graph, type_node[0])["__0__"]
                if (
                    len(type_node) > 0
                    and shard.graph.nodes[type_var].get("label_type")
                    == "identifier"
                ):
                    var_value = get_variable_attribute(
                        shard,
                        shard.graph.nodes[type_var].get("label_text"),
                        "text",
                    )
                elif (
                    len(type_node) > 0
                    and shard.graph.nodes[type_var].get("label_type")
                    == "invocation_expression"
                ):
                    var_value = node_to_str(shard.graph, str(type_var))

                var_items = var_value.split("(") if len(var_value) > 0 else []
                for _class in (
                    shard.metadata.c_sharp.classes.values()
                    if shard.metadata.c_sharp
                    else []
                ):
                    for _method in _class.methods.values():
                        if (
                            len(var_items) > 1
                            and var_items[0] == "Type.GetType"
                            and _method.parameters
                            and var_items[1].replace(")", "")
                            in _method.parameters.keys()
                            and _method.parameters[
                                var_items[1].replace(")", "")
                            ].type_name
                            == "HttpRequest"
                        ):
                            yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f096.insecure_deserialization",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=core_model.MethodsEnum.CS_XML_SERIAL,
    )


def js_deserialization(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_JS_DESERIALIZATION
    c_sharp = graph_model.GraphShardMetadataLanguage.CSHARP
    finding = method.value.finding

    serializer = {"JavaScriptSerializer"}

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            for n_id in yield_shard_object_creation(shard, serializer):
                graph = shard.syntax_graph
                for path in get_backward_paths(graph, n_id):
                    if (
                        evaluation := evaluate(
                            c_sharp, finding, graph, path, n_id
                        )
                    ) and evaluation.danger:
                        yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f096.js_deserialization",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
