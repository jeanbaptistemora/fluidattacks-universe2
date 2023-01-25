from lib_root.utilities.c_sharp import (
    get_first_member_syntax_graph,
    yield_syntax_graph_object_creation,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    Graph,
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
    get_object_identifiers,
)
from typing import (
    Iterable,
    List,
)
from utils import (
    graph as g,
)


def is_serializer_dangerous(graph: Graph, nid: NId) -> bool:
    method = MethodsEnum.CS_XML_SERIAL
    rules = {"Type.GetType", "HttpRequest"}

    for path in get_backward_paths(graph, nid):
        evaluation = evaluate(method, graph, path, nid)
        if evaluation and evaluation.danger and evaluation.triggers == rules:
            return True
    return False


def is_deserialization_dangerous(graph: Graph, nid: NId) -> bool:
    method = MethodsEnum.CS_JS_DESERIALIZATION
    for path in get_backward_paths(graph, nid):
        evaluation = evaluate(method, graph, path, nid)
        if evaluation and evaluation.danger:
            return True
    return False


def is_type_handle_dangerous(
    graph: Graph, member: NId, obj_names: List[str]
) -> bool:
    method = MethodsEnum.CS_TYPE_NAME_HANDLING

    fr_memb = get_first_member_syntax_graph(graph, member)
    last_memb = graph.nodes[member].get("member")
    if (
        graph.nodes[fr_memb].get("label_type") == "SymbolLookup"
        and graph.nodes[fr_memb].get("symbol") in obj_names
        and last_memb == "TypeNameHandling"
        and (pred := g.pred_ast(graph, member)[0])
        and (assign_id := g.match_ast(graph, pred)["__1__"])
    ):
        for path in get_backward_paths(graph, assign_id):
            evaluation = evaluate(method, graph, path, assign_id)
            if evaluation and evaluation.danger:
                return True

    return False


# https://docs.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-security-guide
def insecure_deserialization(
    graph_db: GraphDB,
) -> Vulnerabilities:
    danger_objects = {
        "BinaryFormatter",
        "SoapFormatter",
        "NetDataContractSerializer",
        "LosFormatter",
        "ObjectStateFormatter",
    }

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.CSHARP,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for nid in yield_syntax_graph_object_creation(
                graph, danger_objects
            ):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.096.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_INSECURE_DESERIAL,
    )


def check_xml_serializer(
    graph_db: GraphDB,
) -> Vulnerabilities:
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for nid in yield_syntax_graph_object_creation(
                graph, {"XmlSerializer"}
            ):
                if is_serializer_dangerous(graph, nid):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f096.insecure_deserialization",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_XML_SERIAL,
    )


def js_deserialization(
    graph_db: GraphDB,
) -> Vulnerabilities:
    c_sharp = GraphLanguage.CSHARP
    serializer = {"JavaScriptSerializer"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in yield_syntax_graph_object_creation(graph, serializer):
                if is_deserialization_dangerous(graph, n_id):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f096.js_deserialization",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_JS_DESERIALIZATION,
    )


def type_name_handling(
    graph_db: GraphDB,
) -> Vulnerabilities:
    c_sharp = GraphLanguage.CSHARP
    serializer = {"JsonSerializerSettings"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            serial_objs = get_object_identifiers(graph, serializer)

            for m_id in g.matching_nodes(graph, label_type="MemberAccess"):
                if is_type_handle_dangerous(graph, m_id, serial_objs):
                    yield shard, m_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f096.type_name_handling",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_TYPE_NAME_HANDLING,
    )
