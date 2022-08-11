from lib_root.utilities.c_sharp import (
    get_first_member_syntax_graph,
    get_syntax_object_identifiers,
    yield_syntax_graph_object_creation,
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
    method = core_model.MethodsEnum.CS_XML_SERIAL

    rules = {"Type.GetType", "HttpRequest"}

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for nid in yield_syntax_graph_object_creation(
                graph, {"XmlSerializer"}
            ):
                for path in get_backward_paths(graph, nid):
                    evaluation = evaluate(method, graph, path, nid)
                    if (
                        evaluation
                        and evaluation.danger
                        and evaluation.triggers == rules
                    ):
                        yield shard, nid

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

    serializer = {"JavaScriptSerializer"}

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in yield_syntax_graph_object_creation(graph, serializer):
                graph = shard.syntax_graph
                for path in get_backward_paths(graph, n_id):
                    if (
                        evaluation := evaluate(method, graph, path, n_id)
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

    serializer = {"JsonSerializerSettings"}

    def n_ids() -> graph_model.GraphShardNodes:

        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue

            graph = shard.syntax_graph
            serial_objs = get_syntax_object_identifiers(graph, serializer)
            for member in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="MemberAccess"),
            ):
                fr_memb = get_first_member_syntax_graph(graph, member)
                last_memb = graph.nodes[member].get("member")
                if (
                    graph.nodes[fr_memb].get("label_type") == "SymbolLookup"
                    and graph.nodes[fr_memb].get("symbol") in serial_objs
                    and last_memb == "TypeNameHandling"
                    and (pred := g.pred_ast(graph, member)[0])
                    and (assign := g.match_ast(graph, pred)["__1__"])
                ):
                    for path in get_backward_paths(graph, assign):
                        if (
                            evaluation := evaluate(method, graph, path, assign)
                        ) and evaluation.danger:
                            yield shard, member

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f096.type_name_handling",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
