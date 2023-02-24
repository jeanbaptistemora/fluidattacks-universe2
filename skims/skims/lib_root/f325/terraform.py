from aws.iam.structure import (
    is_action_permissive,
    is_resource_permissive,
)
from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
)
import json
from lib_root.f325.utils import (
    _policy_has_excessive_permissions,
    _policy_has_excessive_permissions_json_encode,
    _policy_has_excessive_permissions_policy_document,
)
from lib_root.utilities.terraform import (
    get_argument,
    get_attr_inside_attrs,
    get_attribute,
    get_list_from_node,
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


def _kms_key_has_master_keys_exposed_to_everyone_in_json(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    child_id = graph.nodes[nid]["arguments_id"]
    statements, _, stmt_id = get_attribute(graph, child_id, "Statement")
    if statements:
        value_id = graph.nodes[stmt_id]["value_id"]
        for c_id in adj_ast(graph, value_id, label_type="Object"):
            _, effect_val, _ = get_attribute(graph, c_id, "Effect")
            aws, aws_val, aws_id = get_attr_inside_attrs(
                graph,
                c_id,
                ["Principal", "AWS"],
            )
            if aws and effect_val == "Allow" and aws_val == "*":
                yield aws_id


def _aux_kms_key_exposed_to_everyone(
    attr_val: str, attr_id: NId
) -> Iterator[NId]:
    dict_value = json.loads(attr_val)
    statements = get_dict_values(dict_value, "Statement")
    for stmt in statements if isinstance(statements, list) else []:
        effect = stmt.get("Effect")
        aws = get_dict_values(stmt, "Principal", "AWS")
        if effect == "Allow" and aws and aws == "*":
            yield attr_id


def _kms_key_has_master_keys_exposed_to_everyone(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    attr, attr_val, attr_id = get_attribute(graph, nid, "policy")
    if attr:
        value_id = graph.nodes[attr_id]["value_id"]
        if graph.nodes[value_id]["label_type"] == "Literal":
            yield from _aux_kms_key_exposed_to_everyone(attr_val, attr_id)
        elif (
            graph.nodes[value_id]["label_type"] == "MethodInvocation"
            and graph.nodes[value_id]["expression"] == "jsonencode"
        ):
            yield from _kms_key_has_master_keys_exposed_to_everyone_in_json(
                graph, value_id
            )


def _iam_has_wildcard_resource_on_write_action_policy_resource(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    for stmt in iter_statements_from_policy_document(graph, nid):
        if _policy_has_excessive_permissions_policy_document(graph, stmt):
            yield stmt


def _aux_iam_has_wildcard_resource_on_write_action(
    attr_val: str, attr_id: NId
) -> Iterator[NId]:
    dict_value = json.loads(attr_val)
    statements = get_dict_values(dict_value, "Statement")
    for stmt in statements if isinstance(statements, list) else []:
        if _policy_has_excessive_permissions(stmt):
            yield attr_id


def _iam_wildcard_res_on_write_action_in_jsonencode(
    graph: Graph,
    nid: NId,
) -> Iterator[NId]:
    child_id = graph.nodes[nid]["arguments_id"]
    statements, _, stmt_id = get_attribute(graph, child_id, "Statement")
    if statements:
        value_id = graph.nodes[stmt_id]["value_id"]
        for c_id in adj_ast(graph, value_id, label_type="Object"):
            if _policy_has_excessive_permissions_json_encode(graph, c_id):
                yield c_id


def _iam_has_wildcard_resource_on_write_action(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    if graph.nodes[nid]["name"] == "aws_iam_policy_document":
        yield from _iam_has_wildcard_resource_on_write_action_policy_resource(
            graph, nid
        )
    else:
        attr, attr_val, attr_id = get_attribute(graph, nid, "policy")
        if attr:
            value_id = graph.nodes[attr_id]["value_id"]
            if graph.nodes[value_id]["label_type"] == "Literal":
                yield from _aux_iam_has_wildcard_resource_on_write_action(
                    attr_val, attr_id
                )
            elif (
                graph.nodes[value_id]["label_type"] == "MethodInvocation"
                and graph.nodes[value_id]["expression"] == "jsonencode"
            ):
                yield from _iam_wildcard_res_on_write_action_in_jsonencode(
                    graph, value_id
                )


def _permissive_policy_in_jsonencode(graph: Graph, nid: NId) -> Iterator[NId]:
    child_id = graph.nodes[nid]["arguments_id"]
    statements, _, stmt_id = get_attribute(graph, child_id, "Statement")
    if statements:
        value_id = graph.nodes[stmt_id]["value_id"]
        for c_id in adj_ast(graph, value_id, label_type="Object"):
            _, effect_val, _ = get_attribute(graph, c_id, "Effect")
            principal = get_argument(graph, c_id, "Principal")
            condition = get_argument(graph, c_id, "Condition")
            if effect_val == "Allow" and not principal and not condition:
                _, _, action_id = get_attribute(graph, c_id, "Action")
                _, _, resources_id = get_attribute(graph, c_id, "Resource")
                action_list = get_list_from_node(graph, action_id)
                resources_list = get_list_from_node(graph, resources_id)
                if all(
                    (
                        any(map(is_action_permissive, action_list)),
                        any(map(is_resource_permissive, resources_list)),
                    )
                ):
                    yield c_id


def _permissive_policy_policy_resource(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    for stmt in iter_statements_from_policy_document(graph, nid):
        effect, effect_val, _ = get_attribute(graph, stmt, "effect")
        condition = get_argument(graph, nid, "condition")
        principal = get_argument(graph, nid, "principals")
        if (
            (effect_val == "Allow" or effect is None)
            and not condition
            and not principal
        ):
            _, _, action_id = get_attribute(graph, stmt, "actions")
            _, _, resources_id = get_attribute(graph, stmt, "resources")
            action_list = get_list_from_node(graph, action_id)
            resources_list = get_list_from_node(graph, resources_id)
            if all(
                (
                    any(map(is_action_permissive, action_list)),
                    any(map(is_resource_permissive, resources_list)),
                )
            ):
                yield stmt


def _aux_permissive_policy(
    attr_val: str,
    attr_id: NId,
) -> Iterator[NId]:
    dict_value = json.loads(attr_val)
    statements = get_dict_values(dict_value, "Statement")
    for stmt in statements if isinstance(statements, list) else []:
        effect = stmt.get("Effect")
        principal = stmt.get("Principal")
        condition = stmt.get("Condition")
        if effect == "Allow" and not principal and not condition:
            actions = stmt.get("Action", [])
            resource = stmt.get("Resource", [])
            if isinstance(actions, str):
                actions = [actions]
            if isinstance(resource, str):
                resource = [resource]
            if all(
                (
                    any(map(is_action_permissive, actions)),
                    any(map(is_resource_permissive, resource)),
                )
            ):
                yield attr_id


def _permissive_policy(graph: Graph, nid: NId) -> Iterator[NId]:
    if graph.nodes[nid]["name"] == "aws_iam_policy_document":
        yield from _permissive_policy_policy_resource(graph, nid)
    else:
        attr, attr_val, attr_id = get_attribute(graph, nid, "policy")
        if attr:
            value_id = graph.nodes[attr_id]["value_id"]
            if graph.nodes[value_id]["label_type"] == "Literal":
                yield from _aux_permissive_policy(attr_val, attr_id)
            elif (
                graph.nodes[value_id]["label_type"] == "MethodInvocation"
                and graph.nodes[value_id]["expression"] == "jsonencode"
            ):
                yield from _permissive_policy_in_jsonencode(graph, value_id)


def tfm_permissive_policy(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_PERMISSIVE_POLICY

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
                for report in _permissive_policy(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f325_aws.permissive_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_iam_has_wildcard_resource_on_write_action(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_IAM_WILDCARD_WRITE

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
                for report in _iam_has_wildcard_resource_on_write_action(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f325.iam_has_wildcard_resource_on_write_action",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_kms_key_has_master_keys_exposed_to_everyone(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_KMS_MASTER_KEYS_EXPOSED

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_kms_key"):
                for report in _kms_key_has_master_keys_exposed_to_everyone(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=(
            "src.lib_path.f325.kms_key_has_master_keys_exposed_to_everyone"
        ),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
