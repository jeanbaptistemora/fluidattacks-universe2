from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
)
from lib_root.utilities.cloudformation import (
    get_attribute,
    iterate_group_resources,
    iterate_iam_policy_documents,
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
) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    policies, _, policies_id = get_attribute(graph, val_id, "Policies")
    if policies:
        policies_attrs = graph.nodes[policies_id]["value_id"]
        for pol in adj_ast(graph, policies_attrs):
            policy_name, _, pn_id = get_attribute(graph, pol, "PolicyName")
            if policy_name:
                yield pn_id


def _admin_policy_attached(graph: Graph, nid: NId) -> Iterator[NId]:
    elevated_policies = {
        "PowerUserAccess",
        "IAMFullAccess",
        "AdministratorAccess",
    }
    value = graph.nodes[nid]["value"]
    if value.split("/")[-1] in elevated_policies:
        yield nid


def _iam_has_full_access_to_ssm(graph: Graph, nid: NId) -> Iterator[NId]:
    effect, effect_val, _ = get_attribute(graph, nid, "Effect")
    action, action_val, action_id = get_attribute(graph, nid, "Action")
    if effect and action and effect_val == "Allow":
        action_attrs = graph.nodes[action_id]["value_id"]
        if graph.nodes[action_attrs]["label_type"] == "ArrayInitializer":
            for act in adj_ast(graph, action_attrs):
                if graph.nodes[act]["value"] == "ssm:*":
                    yield act
        elif action_val == "ssm:*":
            yield action_id


def cfn_iam_has_full_access_to_ssm(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_FULL_ACCESS_SSM

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_iam_policy_documents(graph):
                for report in _iam_has_full_access_to_ssm(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031.iam_has_full_access_to_ssm",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_admin_policy_attached(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_ADMIN_POLICY_ATTACHED

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_group_resources(graph, "AWS::IAM"):
                for report in _admin_policy_attached(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031_aws.permissive_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_iam_user_missing_role_based_security(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_MISSING_SECURITY

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "AWS::IAM::User"):
                for report in _iam_user_missing_role_based_security(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031.iam_user_missing_role_based_security",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
