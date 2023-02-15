from collections.abc import (
    Iterator,
)
from lib_root.utilities.terraform import (
    get_key_value,
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
from utils.graph import (
    adj_ast,
)


def _iam_user_missing_role_based_security(
    graph: Graph, nid: NId
) -> NId | None:
    expected_attr = "name"
    for c_id in adj_ast(graph, nid, label_type="Pair"):
        key, _ = get_key_value(graph, c_id)
        if key == expected_attr:
            return c_id
    return None


def _iam_excessive_privileges(graph: Graph, nid: NId) -> NId | None:
    expected_attr = "managed_policy_arns"
    for c_id in adj_ast(graph, nid, label_type="Pair"):
        key, _ = get_key_value(graph, c_id)
        value_id = graph.nodes[c_id]["value_id"]
        if (
            key == expected_attr
            and graph.nodes[value_id]["label_type"] == "ArrayInitializer"
        ):
            for array_elem in adj_ast(graph, value_id):
                if "AdministratorAccess" in graph.nodes[array_elem]["value"]:
                    return array_elem
    return None


def tfm_iam_user_missing_role_based_security(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_IAM_MISSING_SECURITY

    def n_ids() -> Iterator[GraphShardNode]:
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


def tfm_iam_excessive_privileges(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_ADMIN_MANAGED_POLICIES

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_iam_role"):
                if report := _iam_excessive_privileges(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031_aws.permissive_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
