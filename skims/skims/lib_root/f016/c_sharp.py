from lib_root.utilities.c_sharp import (
    check_member_acces_expression,
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


def weak_protocol(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_WEAK_PROTOCOL

    def n_ids() -> GraphShardNodes:
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
                    in {"Ssl3", "Tls", "None"}
                ):
                    yield shard, member

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f016.serves_content_over_insecure_protocols",
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
