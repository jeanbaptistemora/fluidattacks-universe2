from collections.abc import (
    Iterator,
)
import json
from lib_root.utilities.terraform import (
    get_attr_inside_attrs,
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
