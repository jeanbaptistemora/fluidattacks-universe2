from collections.abc import (
    Iterable,
    Iterator,
)
from lib_root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
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
    MetadataGraphShardNode,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
    get_vulnerabilities_from_n_ids_metadata,
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
from utils.string import (
    split_on_first_dot as split_fr,
)


def is_point_manager_vulnerable(
    method: MethodsEnum, graph: Graph, n_id: str
) -> NId | None:
    member_str = (
        "Switch.System.ServiceModel."
        "DisableUsingServicePointManagerSecurityProtocols"
    )
    rules = {
        member_str,
        "true",
    }
    pred = g.pred_ast(graph, n_id)[0]
    if get_node_evaluation_results(method, graph, pred, rules):
        return pred
    return None


def is_insecure_protocol(
    graph: Graph, n_id: str, obj_identifiers: Iterable[str]
) -> bool:
    method = MethodsEnum.CS_INSECURE_SHARED_ACCESS_PROTOCOL
    if (
        (split_expr := split_fr(graph.nodes[n_id].get("expression")))
        and split_expr[0] in obj_identifiers
        and split_expr[1] == "GetSharedAccessSignature"
        and get_node_evaluation_results(method, graph, n_id, set())
    ):
        return True
    return False


def weak_protocol(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.CS_WEAK_PROTOCOL
    weak_protocols = ["Ssl3", "Tls", "Tls11", "None"]

    def n_ids() -> Iterator[MetadataGraphShardNode]:
        metadata = {}
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for nid in g.matching_nodes(graph, label_type="MemberAccess"):
                protocol = graph.nodes[nid].get("member")
                if (
                    graph.nodes[nid].get("expression")
                    == "SecurityProtocolType"
                    and protocol in weak_protocols
                ):
                    metadata["what"] = protocol
                    metadata["desc_params"] = {"protocol": protocol}
                    yield shard, nid, metadata

    return get_vulnerabilities_from_n_ids_metadata(
        desc_key="src.lib_root.f016.csharp_weak_protocol",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def service_point_manager_disabled(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.CS_SERVICE_POINT_MANAGER_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for member in yield_syntax_graph_member_access(
                graph, {"AppContext"}
            ):
                if graph.nodes[member]["member"] == "SetSwitch" and (
                    nid := is_point_manager_vulnerable(method, graph, member)
                ):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f016.service_point_manager_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def insecure_shared_access_protocol(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.CS_INSECURE_SHARED_ACCESS_PROTOCOL

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            obj_identifiers = get_object_identifiers(graph, {"CloudFile"})
            for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
                if is_insecure_protocol(graph, n_id, obj_identifiers):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f016.insecure_shared_access_protocol",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def httpclient_no_revocation_list(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.CS_HTTPCLIENT_NO_REVOCATION_LIST

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(graph, label_type="ObjectCreation"):
                if graph.nodes[n_id].get(
                    "name"
                ) == "HttpClient" and get_node_evaluation_results(
                    method, graph, n_id, set()
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f016.httpclient_no_revocation_list",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
