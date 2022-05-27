from lib_root.utilities.c_sharp import (
    check_member_acces_expression,
    get_object_identifiers,
    yield_shard_member_access,
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
            for member in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(
                    label_type="member_access_expression"
                ),
            ):
                c_ident = g.get_ast_childs(shard.graph, member, "identifier")
                if (
                    len(c_ident) == 2
                    and shard.graph.nodes[c_ident[0]]["label_text"]
                    == "SecurityProtocolType"
                    and shard.graph.nodes[c_ident[1]]["label_text"]
                    in {"Ssl3", "Tls", "Tls11", "None"}
                ):
                    protocol = shard.graph.nodes[c_ident[1]]["label_text"]

                    metadata["what"] = protocol
                    metadata["desc_params"] = {"protocol": protocol}

                    yield shard, member, metadata

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
    finding = method.value.finding
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

            for member in yield_shard_member_access(shard, {"AppContext"}):
                if not check_member_acces_expression(
                    shard, member, "SetSwitch"
                ):
                    continue
                graph = shard.syntax_graph
                pred = g.pred_ast(shard.graph, member)[0]
                for path in get_backward_paths(graph, pred):
                    evaluation = evaluate(c_sharp, finding, graph, path, pred)
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
    finding = method.value.finding
    c_sharp = GraphShardMetadataLanguage.CSHARP

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue

            obj_identifiers = get_object_identifiers(shard, {"CloudFile"})
            s_graph = shard.syntax_graph

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
                    evaluation = evaluate(c_sharp, finding, s_graph, path, nid)
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
    finding = method.value.finding
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
                if not s_graph.nodes[nid].get("name") == "HttpClient":
                    continue
                for path in get_backward_paths(s_graph, nid):
                    evaluation = evaluate(c_sharp, finding, s_graph, path, nid)
                    if evaluation and evaluation.danger:
                        yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f016.httpclient_no_revocation_list",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
