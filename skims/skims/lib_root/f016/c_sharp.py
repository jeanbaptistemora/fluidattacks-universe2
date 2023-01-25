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
    GraphShardMetadataLanguage,
    GraphShardNode,
    MetadataGraphShardNode,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
    get_vulnerabilities_from_n_ids_metadata,
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
    Optional,
)
from utils import (
    graph as g,
)
from utils.string import (
    split_on_first_dot as split_fr,
)


def get_eval_danger(graph: Graph, n_id: str, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def is_point_manager_vulnerable(graph: Graph, n_id: str) -> Optional[NId]:
    method = MethodsEnum.CS_SERVICE_POINT_MANAGER_DISABLED
    member_str = (
        "Switch.System.ServiceModel."
        + "DisableUsingServicePointManagerSecurityProtocols"
    )
    rules = {
        member_str,
        "true",
    }
    pred = g.pred_ast(graph, n_id)[0]
    for path in get_backward_paths(graph, pred):
        evaluation = evaluate(method, graph, path, pred)
        if evaluation and evaluation.danger and evaluation.triggers == rules:
            return pred
    return None


def is_insecure_protocol(
    graph: Graph, n_id: str, obj_identifiers: List[str]
) -> bool:
    method = MethodsEnum.CS_INSECURE_SHARED_ACCESS_PROTOCOL
    if (
        (split_expr := split_fr(graph.nodes[n_id].get("expression")))
        and split_expr[0] in obj_identifiers
        and split_expr[1] == "GetSharedAccessSignature"
        and get_eval_danger(graph, n_id, method)
    ):
        return True
    return False


def weak_protocol(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_WEAK_PROTOCOL

    def n_ids() -> Iterable[MetadataGraphShardNode]:
        metadata = {}
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.CSHARP,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for nid in g.matching_nodes(
                graph,
                label_type="MemberAccess",
            ):

                protocol = graph.nodes[nid].get("member")
                if graph.nodes[nid].get(
                    "expression"
                ) == "SecurityProtocolType" and protocol in [
                    "Ssl3",
                    "Tls",
                    "Tls11",
                    "None",
                ]:
                    metadata["what"] = protocol
                    metadata["desc_params"] = {"protocol": protocol}

                    yield shard, nid, metadata

    return get_vulnerabilities_from_n_ids_metadata(
        desc_key="src.lib_root.f016.csharp_weak_protocol",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def service_point_manager_disabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_SERVICE_POINT_MANAGER_DISABLED
    c_sharp = GraphShardMetadataLanguage.CSHARP

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for member in yield_syntax_graph_member_access(
                graph, {"AppContext"}
            ):
                if graph.nodes[member]["member"] == "SetSwitch" and (
                    nid := is_point_manager_vulnerable(graph, member)
                ):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f016.service_point_manager_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def insecure_shared_access_protocol(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_INSECURE_SHARED_ACCESS_PROTOCOL
    c_sharp = GraphShardMetadataLanguage.CSHARP

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            obj_identifiers = get_object_identifiers(graph, {"CloudFile"})

            for nid in g.matching_nodes(
                graph,
                label_type="MethodInvocation",
            ):
                if is_insecure_protocol(graph, nid, obj_identifiers):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f016.insecure_shared_access_protocol",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def httpclient_no_revocation_list(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_HTTPCLIENT_NO_REVOCATION_LIST
    c_sharp = GraphShardMetadataLanguage.CSHARP

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue

            graph = shard.syntax_graph

            for nid in g.matching_nodes(
                graph,
                label_type="ObjectCreation",
            ):
                if graph.nodes[nid].get(
                    "name"
                ) == "HttpClient" and get_eval_danger(graph, nid, method):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f016.httpclient_no_revocation_list",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
