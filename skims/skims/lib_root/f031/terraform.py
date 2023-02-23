from aws.iam.structure import (
    is_action_permissive,
    is_public_principal,
    is_resource_permissive,
)
from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
)
import json
from lib_root.f031.utils import (
    _iam_user_missing_role_based_security,
    action_has_full_access_to_ssm,
    is_s3_action_writeable,
)
from lib_root.utilities.terraform import (
    get_attribute,
    get_list_from_node,
    get_principals,
    iter_statements_from_policy_document,
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
from utils.function import (
    get_dict_values,
)
from utils.graph import (
    adj_ast,
)


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


def _bucket_policy_allows_public_access_in_jsonencode(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    child_id = graph.nodes[nid]["arguments_id"]
    statements, _, stmt_id = get_attribute(graph, child_id, "Statement")
    if statements:
        value_id = graph.nodes[stmt_id]["value_id"]
        for c_id in adj_ast(graph, value_id, label_type="Object"):
            _, effect_val, _ = get_attribute(graph, c_id, "Effect")
            _, principal_val, _ = get_attribute(graph, c_id, "Principal")
            actions, _, action_id = get_attribute(graph, c_id, "Action")
            if actions:
                action_list = get_list_from_node(graph, action_id)
                if (
                    effect_val == "Allow"
                    and is_public_principal(principal_val)
                    and is_s3_action_writeable(action_list)
                ):
                    yield c_id


def _bucket_policy_allows_public_access_policy_resource(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    for stmt in iter_statements_from_policy_document(graph, nid):
        effect, effect_val, _ = get_attribute(graph, stmt, "effect")
        action, _, action_id = get_attribute(graph, stmt, "actions")
        principal = get_principals(graph, stmt)
        if action:
            action_list = get_list_from_node(graph, action_id)
            if (
                (effect_val == "Allow" or effect is None)
                and is_public_principal(principal)
                and is_s3_action_writeable(action_list)
            ):
                yield stmt


def _aux_bucket_policy_public(attr_val: str, attr_id: NId) -> Iterator[NId]:
    dict_value = json.loads(attr_val)
    statements = get_dict_values(dict_value, "Statement")
    for stmt in statements if isinstance(statements, list) else []:
        effect = stmt.get("Effect")
        principal = stmt.get("Principal", "")
        actions = stmt.get("Action", [])
        if (
            effect == "Allow"
            and is_public_principal(principal)
            and is_s3_action_writeable(actions)
        ):
            yield attr_id


def _bucket_policy_allows_public_access(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    if graph.nodes[nid]["name"] == "aws_iam_policy_document":
        yield from _bucket_policy_allows_public_access_policy_resource(
            graph, nid
        )
    else:
        attr, attr_val, attr_id = get_attribute(graph, nid, "policy")
        if attr:
            value_id = graph.nodes[attr_id]["value_id"]
            if graph.nodes[value_id]["label_type"] == "Literal":
                yield from _aux_bucket_policy_public(attr_val, attr_id)
            elif (
                graph.nodes[value_id]["label_type"] == "MethodInvocation"
                and graph.nodes[value_id]["expression"] == "jsonencode"
            ):
                yield from _bucket_policy_allows_public_access_in_jsonencode(
                    graph, value_id
                )


def _iam_has_full_access_to_ssm_in_jsonencode(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    child_id = graph.nodes[nid]["arguments_id"]
    statements, _, stmt_id = get_attribute(graph, child_id, "Statement")
    if statements:
        value_id = graph.nodes[stmt_id]["value_id"]
        for c_id in adj_ast(graph, value_id, label_type="Object"):
            _, effect_val, _ = get_attribute(graph, c_id, "Effect")
            actions, _, action_id = get_attribute(graph, c_id, "Action")
            if actions:
                action_list = get_list_from_node(graph, action_id)
                if effect_val == "Allow" and action_has_full_access_to_ssm(
                    action_list
                ):
                    yield c_id


def _iam_has_full_access_to_ssm_policy_resource(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    for stmt in iter_statements_from_policy_document(graph, nid):
        effect, effect_val, _ = get_attribute(graph, stmt, "effect")
        action, _, action_id = get_attribute(graph, stmt, "actions")
        if action:
            action_list = get_list_from_node(graph, action_id)
            if (
                effect_val == "Allow" or effect is None
            ) and action_has_full_access_to_ssm(action_list):
                yield stmt


def _aux_iam_has_full_access_to_ssm(
    attr_val: str, attr_id: NId
) -> Iterator[NId]:
    dict_value = json.loads(attr_val)
    statements = get_dict_values(dict_value, "Statement")
    for stmt in statements if isinstance(statements, list) else []:
        effect = stmt.get("Effect")
        actions = stmt.get("Action", [])
        if effect == "Allow" and action_has_full_access_to_ssm(actions):
            yield attr_id


def _iam_has_full_access_to_ssm(graph: Graph, nid: NId) -> Iterator[NId]:
    if graph.nodes[nid]["name"] == "aws_iam_policy_document":
        yield from _iam_has_full_access_to_ssm_policy_resource(graph, nid)
    else:
        attr, attr_val, attr_id = get_attribute(graph, nid, "policy")
        if attr:
            value_id = graph.nodes[attr_id]["value_id"]
            if graph.nodes[value_id]["label_type"] == "Literal":
                yield from _aux_iam_has_full_access_to_ssm(attr_val, attr_id)
            elif (
                graph.nodes[value_id]["label_type"] == "MethodInvocation"
                and graph.nodes[value_id]["expression"] == "jsonencode"
            ):
                yield from _iam_has_full_access_to_ssm_in_jsonencode(
                    graph, value_id
                )


def _negative_statement_in_jsonencode(graph: Graph, nid: NId) -> Iterator[NId]:
    child_id = graph.nodes[nid]["arguments_id"]
    statements, _, stmt_id = get_attribute(graph, child_id, "Statement")
    if statements:
        value_id = graph.nodes[stmt_id]["value_id"]
        for c_id in adj_ast(graph, value_id, label_type="Object"):
            _, effect_val, _ = get_attribute(graph, c_id, "Effect")
            if effect_val == "Allow":
                actions, _, action_id = get_attribute(graph, c_id, "NotAction")
                resources, _, resources_id = get_attribute(
                    graph, c_id, "NotResource"
                )
                action_list = get_list_from_node(graph, action_id)
                resources_list = get_list_from_node(graph, resources_id)
                if (
                    actions and not any(map(is_action_permissive, action_list))
                ) or (
                    resources
                    and not any(map(is_resource_permissive, resources_list))
                ):
                    yield c_id


def _negative_statement_policy_resource(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    for stmt in iter_statements_from_policy_document(graph, nid):
        effect, effect_val, _ = get_attribute(graph, stmt, "effect")
        if effect_val == "Allow" or effect is None:
            actions, _, action_id = get_attribute(graph, stmt, "not_actions")
            resources, _, resources_id = get_attribute(
                graph, stmt, "not_resources"
            )
            action_list = get_list_from_node(graph, action_id)
            resources_list = get_list_from_node(graph, resources_id)
            if (
                actions and not any(map(is_action_permissive, action_list))
            ) or (
                resources
                and not any(map(is_resource_permissive, resources_list))
            ):
                yield stmt


def _aux_negative_statement(attr_val: str, attr_id: NId) -> Iterator[NId]:
    dict_value = json.loads(attr_val)
    statements = get_dict_values(dict_value, "Statement")
    for stmt in statements if isinstance(statements, list) else []:
        effect = stmt.get("Effect")
        if effect == "Allow":
            actions = stmt.get("NotAction")
            resource = stmt.get("NotResource")
            if (actions and not any(map(is_action_permissive, actions))) or (
                resource and not any(map(is_resource_permissive, resource))
            ):
                yield attr_id


def _negative_statement(graph: Graph, nid: NId) -> Iterator[NId]:
    if graph.nodes[nid]["name"] == "aws_iam_policy_document":
        yield from _negative_statement_policy_resource(graph, nid)
    else:
        attr, attr_val, attr_id = get_attribute(graph, nid, "policy")
        if attr:
            value_id = graph.nodes[attr_id]["value_id"]
            if graph.nodes[value_id]["label_type"] == "Literal":
                yield from _aux_negative_statement(attr_val, attr_id)
            elif (
                graph.nodes[value_id]["label_type"] == "MethodInvocation"
                and graph.nodes[value_id]["expression"] == "jsonencode"
            ):
                yield from _negative_statement_in_jsonencode(graph, value_id)


def terraform_negative_statement(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_NEGATIVE_STATEMENT

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in chain(
                iterate_resource(graph, "aws_iam_group_policy"),
                iterate_resource(graph, "aws_iam_policy"),
                iterate_resource(graph, "aws_iam_role_policy"),
                iterate_resource(graph, "aws_iam_user_policy"),
                iterate_resource(graph, "aws_iam_policy_document"),
            ):
                for report in _negative_statement(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031_aws.negative_statement",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_iam_has_full_access_to_ssm(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_IAM_FULL_ACCESS_SSM

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in chain(
                iterate_resource(graph, "aws_iam_group_policy"),
                iterate_resource(graph, "aws_iam_policy"),
                iterate_resource(graph, "aws_iam_role_policy"),
                iterate_resource(graph, "aws_iam_user_policy"),
                iterate_resource(graph, "aws_iam_policy_document"),
            ):
                for report in _iam_has_full_access_to_ssm(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031.iam_has_full_access_to_ssm",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_bucket_policy_allows_public_access(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_BUCKET_ALLOWS_PUBLIC

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in chain(
                iterate_resource(graph, "aws_iam_group_policy"),
                iterate_resource(graph, "aws_iam_policy"),
                iterate_resource(graph, "aws_iam_role_policy"),
                iterate_resource(graph, "aws_iam_user_policy"),
                iterate_resource(graph, "aws_iam_policy_document"),
            ):
                for report in _bucket_policy_allows_public_access(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031.bucket_policy_allows_public_access",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


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
