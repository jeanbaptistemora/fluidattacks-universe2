from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
)
from lib_root.utilities.terraform import (
    get_attribute,
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
    expected_attr = get_attribute(graph, nid, "name")
    if expected_attr[0]:
        return expected_attr[2]
    return None


def _iam_excessive_privileges(graph: Graph, nid: NId) -> NId | None:
    _, _, attr_id = get_attribute(graph, nid, "managed_policy_arns")
    value_id = graph.nodes[attr_id]["value_id"]
    if graph.nodes[value_id]["label_type"] == "ArrayInitializer":
        for array_elem in adj_ast(graph, value_id):
            if "AdministratorAccess" in graph.nodes[array_elem]["value"]:
                return array_elem
    return None


def _admin_policy_attached(graph: Graph, nid: NId) -> NId | None:
    elevated_policies = {
        "PowerUserAccess",
        "IAMFullAccess",
        "AdministratorAccess",
    }
    policy, pol_attr, pol_id = get_attribute(graph, nid, "policy_arn")
    if policy and pol_attr.split("/")[-1] in elevated_policies:
        return pol_id
    return None


def tfm_admin_policy_attached(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_ADMIN_POLICY

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in chain(
                iterate_resource(graph, "aws_iam_group_policy_attachment"),
                iterate_resource(graph, "aws_iam_policy_attachment"),
                iterate_resource(graph, "aws_iam_role_policy_attachment"),
                iterate_resource(graph, "aws_iam_user_policy_attachment"),
            ):
                if report := _admin_policy_attached(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031_aws.permissive_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


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
