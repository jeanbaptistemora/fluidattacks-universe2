from lib_root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage,
    GraphShardNodes,
    MetadataGraphShardNodes,
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
from utils import (
    graph as g,
)
from utils.string import (
    split_on_first_dot as split_fr,
)


def weak_protocol(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_WEAK_PROTOCOL

    def n_ids() -> MetadataGraphShardNodes:
        metadata = {}
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.CSHARP,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for nid in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="MemberAccess"),
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
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_SERVICE_POINT_MANAGER_DISABLED
    c_sharp = GraphShardMetadataLanguage.CSHARP

    member_str = (
        "Switch.System.ServiceModel."
        + "DisableUsingServicePointManagerSecurityProtocols"
    )

    rules = {
        member_str,
        "true",
    }

    def n_ids() -> GraphShardNodes:

        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for member in yield_syntax_graph_member_access(
                graph, {"AppContext"}
            ):
                if graph.nodes[member]["member"] != "SetSwitch":
                    continue

                pred = g.pred_ast(shard.graph, member)[0]
                for path in get_backward_paths(graph, pred):
                    evaluation = evaluate(method, graph, path, pred)
                    if (
                        evaluation
                        and evaluation.danger
                        and evaluation.triggers == rules
                    ):
                        yield shard, pred

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f016.service_point_manager_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def insecure_shared_access_protocol(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_INSECURE_SHARED_ACCESS_PROTOCOL
    c_sharp = GraphShardMetadataLanguage.CSHARP

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            s_graph = shard.syntax_graph

            obj_identifiers = get_object_identifiers(s_graph, {"CloudFile"})

            for nid in g.filter_nodes(
                s_graph,
                nodes=shard.syntax_graph.nodes,
                predicate=g.pred_has_labels(
                    label_type="MethodInvocation",
                ),
            ):
                if not (
                    (
                        split_expr := split_fr(
                            s_graph.nodes[nid].get("expression")
                        )
                    )
                    and split_expr[0] in obj_identifiers
                    and split_expr[1] == "GetSharedAccessSignature"
                ):
                    continue
                for path in get_backward_paths(s_graph, nid):
                    evaluation = evaluate(method, s_graph, path, nid)
                    if evaluation and evaluation.danger:
                        yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f016.insecure_shared_access_protocol",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def httpclient_no_revocation_list(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_HTTPCLIENT_NO_REVOCATION_LIST
    c_sharp = GraphShardMetadataLanguage.CSHARP

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue

            s_graph = shard.syntax_graph

            for nid in g.filter_nodes(
                s_graph,
                nodes=shard.syntax_graph.nodes,
                predicate=g.pred_has_labels(
                    label_type="ObjectCreation",
                ),
            ):
                if s_graph.nodes[nid].get("name") != "HttpClient":
                    continue
                for path in get_backward_paths(s_graph, nid):
                    evaluation = evaluate(method, s_graph, path, nid)
                    if evaluation and evaluation.danger:
                        yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f016.httpclient_no_revocation_list",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
