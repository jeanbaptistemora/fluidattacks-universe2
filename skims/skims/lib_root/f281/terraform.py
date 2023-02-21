from collections.abc import (
    Iterator,
)
import json
from lib_path.common import (
    FALSE_OPTIONS,
    TRUE_OPTIONS,
)
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


def _bucket_policy_has_secure_transport_in_jsonencode(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    child_id = graph.nodes[nid]["arguments_id"]
    statements, _, stmt_id = get_attribute(graph, child_id, "Statement")
    if statements:
        value_id = graph.nodes[stmt_id]["value_id"]
        for c_id in adj_ast(graph, value_id, label_type="Object"):
            _, effect_val, _ = get_attribute(graph, c_id, "Effect")
            sec_trans, sec_trans_val, sec_trans_id = get_attr_inside_attrs(
                graph,
                c_id,
                ["Condition", "Bool", "aws:SecureTransport"],
            )
            if sec_trans and (
                (effect_val == "Deny" and sec_trans_val in TRUE_OPTIONS)
                or (effect_val == "Allow" and sec_trans_val in FALSE_OPTIONS)
            ):
                yield sec_trans_id


def _aux_bucket_policy_sec_trans(attr_val: str, attr_id: NId) -> Iterator[NId]:
    dict_value = json.loads(attr_val)
    statements = get_dict_values(dict_value, "Statement")
    for stmt in statements if isinstance(statements, list) else []:
        effect = stmt.get("Effect")
        secure_transport = get_dict_values(
            stmt, "Condition", "Bool", "aws:SecureTransport"
        )
        if secure_transport and (
            (effect == "Deny" and secure_transport in TRUE_OPTIONS)
            or (effect == "Allow" and secure_transport in FALSE_OPTIONS)
        ):
            yield attr_id


def _bucket_policy_has_secure_transport(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    attr, attr_val, attr_id = get_attribute(graph, nid, "policy")
    value_id = graph.nodes[attr_id]["value_id"]
    if attr:
        if graph.nodes[value_id]["label_type"] == "Literal":
            yield from _aux_bucket_policy_sec_trans(attr_val, attr_id)
        elif (
            graph.nodes[value_id]["label_type"] == "MethodInvocation"
            and graph.nodes[value_id]["expression"] == "jsonencode"
        ):
            yield from _bucket_policy_has_secure_transport_in_jsonencode(
                graph, value_id
            )


def tfm_bucket_policy_has_secure_transport(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_BUCKET_POLICY_SEC_TRANSPORT

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_s3_bucket_policy"):
                for report in _bucket_policy_has_secure_transport(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f281.bucket_policy_has_secure_transport",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
