from lib_root.utilities.c_sharp import (
    get_first_member,
    get_object_identifiers,
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
from utils import (
    graph as g,
)
from utils.graph.text_nodes import (
    node_to_str,
)
from utils.string import (
    split_on_last_dot as split_last,
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
                type_node = g.get_ast_childs(
                    shard.graph, node, "argument", depth=2
                )
                type_var = g.match_ast(shard.graph, type_node[0])["__0__"]
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


def type_name_handling(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_TYPE_NAME_HANDLING
    c_sharp = graph_model.GraphShardMetadataLanguage.CSHARP
    finding = method.value.finding

    serializer = {"JsonSerializerSettings"}

    def n_ids() -> graph_model.GraphShardNodes:

        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue

            serial_objs = get_object_identifiers(shard, serializer)

            for member in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(
                    label_type="member_access_expression"
                ),
            ):
                fr_member = get_first_member(shard, member)
                last_member = split_last(node_to_str(shard.graph, member))[1]
                if (
                    shard.graph.nodes[fr_member]["label_text"] in serial_objs
                    and last_member == "TypeNameHandling"
                    and (pred := g.pred_ast(shard.graph, member)[0])
                    and (assign := g.match_ast(shard.graph, pred)["__2__"])
                ):
                    for path in get_backward_paths(shard.syntax_graph, assign):
                        graph = shard.syntax_graph
                        if (
                            evaluation := evaluate(
                                c_sharp, finding, graph, path, assign
                            )
                        ) and evaluation.danger:
                            yield shard, member

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f096.type_name_handling",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
