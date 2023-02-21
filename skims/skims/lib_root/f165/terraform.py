from collections.abc import (
    Iterator,
)
import json
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
from utils.function import (
    get_dict_values,
)
from utils.graph import (
    adj_ast,
)


def _iam_role_is_over_privileged_in_jsonencode(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    child_id = graph.nodes[nid]["arguments_id"]
    statements, _, stmt_id = get_attribute(graph, child_id, "Statement")
    if statements:
        value_id = graph.nodes[stmt_id]["value_id"]
        for c_id in adj_ast(graph, value_id, label_type="Object"):
            _, effect_val, _ = get_attribute(graph, c_id, "Effect")
            not_principal, _, np_id = get_attribute(
                graph, c_id, "NotPrincipal"
            )
            if effect_val == "Allow" and not_principal is not None:
                yield np_id


def _iam_role_is_over_privileged(graph: Graph, nid: NId) -> Iterator[NId]:
    attr, attr_val, attr_id = get_attribute(graph, nid, "assume_role_policy")
    value_id = graph.nodes[attr_id]["value_id"]
    if attr and graph.nodes[value_id]["label_type"] == "Literal":
        dict_value = json.loads(attr_val)
        statements = get_dict_values(dict_value, "Statement")
        for stmt in statements if isinstance(statements, list) else []:
            effect = stmt.get("Effect")
            not_principal = get_dict_values(stmt, "NotPrincipal")
            if effect == "Allow" and not_principal:
                yield attr_id
    elif (
        attr
        and graph.nodes[value_id]["label_type"] == "MethodInvocation"
        and graph.nodes[value_id]["expression"] == "jsonencode"
    ):
        yield from _iam_role_is_over_privileged_in_jsonencode(graph, value_id)


def tfm_iam_role_is_over_privileged(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_IAM_ROLE_OVER_PRIVILEGED

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_iam_role"):
                for report in _iam_role_is_over_privileged(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f165.iam_allow_not_principal_trust_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
