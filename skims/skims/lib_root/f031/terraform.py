from lib_root.utilities.terraform import (
    iterate_resource,
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
from typing import (
    Iterable,
    Optional,
)
from utils.graph import (
    adj_ast,
)


def _iam_user_missing_role_based_security(
    graph: Graph, nid: NId
) -> Optional[NId]:
    expected_attr = "name"
    for c_id in adj_ast(graph, nid, label_type="Pair"):
        key_id = graph.nodes[c_id]["key_id"]
        key = graph.nodes[key_id]["value"]
        if key == expected_attr:
            return c_id
    return None


def tfm_iam_user_missing_role_based_security(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_IAM_MISSING_SECURITY

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_iam_user_policy"):
                if report := _iam_user_missing_role_based_security(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031.iam_user_missing_role_based_security",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
