from collections.abc import (
    Iterable,
    Iterator,
)
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
    get_node_evaluation_results,
)
from symbolic_eval.utils import (
    get_object_identifiers,
)
from utils import (
    graph as g,
)


def is_type_handle_dangerous(
    method: MethodsEnum, graph: Graph, member: NId, obj_names: Iterable[str]
) -> bool:
    if (
        graph.nodes[member].get("member") == "TypeNameHandling"
        and (fr_memb := get_first_member_syntax_graph(graph, member))
        and graph.nodes[fr_memb].get("symbol") in obj_names
        and (pred := g.pred_ast(graph, member)[0])
        and (assign_id := g.match_ast(graph, pred)["__1__"])
    ):
        return get_node_evaluation_results(method, graph, assign_id, set())
    return False


# https://docs.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-security-guide
def insecure_deserialization(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.CS_INSECURE_DESERIAL
    danger_objects = {
        "BinaryFormatter",
        "SoapFormatter",
        "NetDataContractSerializer",
        "LosFormatter",
        "ObjectStateFormatter",
    }

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
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
        method=method,
    )


def check_xml_serializer(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.CS_XML_SERIAL
    danger_set = {"Type.GetType", "HttpRequest"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for nid in yield_syntax_graph_object_creation(
                graph, {"XmlSerializer"}
            ):
                if get_node_evaluation_results(method, graph, nid, danger_set):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f096.insecure_deserialization",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def js_deserialization(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.CS_JS_DESERIALIZATION
    serializer = {"JavaScriptSerializer"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in yield_syntax_graph_object_creation(graph, serializer):
                if get_node_evaluation_results(method, graph, n_id, set()):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f096.js_deserialization",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def type_name_handling(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.CS_TYPE_NAME_HANDLING
    serializer = {"JsonSerializerSettings"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            serial_objs = get_object_identifiers(graph, serializer)

            for m_id in g.matching_nodes(graph, label_type="MemberAccess"):
                if is_type_handle_dangerous(method, graph, m_id, serial_objs):
                    yield shard, m_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f096.type_name_handling",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
