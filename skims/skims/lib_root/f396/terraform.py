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
from typing import (
    Iterable,
    Optional,
)
from utils.graph import (
    adj_ast,
)


def _kms_key_is_key_rotation_absent_or_disabled(
    graph: Graph, nid: NId
) -> Optional[NId]:
    en_key_rot = "enable_key_rotation"
    key_spec = "customer_master_key_spec"
    has_attr = False
    insec_id = None
    non_vuln = False

    for b_id in adj_ast(graph, nid, label_type="Pair"):
        key, value = get_key_value(graph, b_id)
        if key == key_spec and value != "SYMMETRIC_DEFAULT":
            non_vuln = True
        if key == en_key_rot:
            has_attr = True
            if value.lower() in {"false", "0"}:
                insec_id = b_id
    if non_vuln:
        return None
    if not has_attr:
        return nid
    if insec_id:
        return insec_id
    return None


def tfm_kms_key_is_key_rotation_absent_or_disabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_KMS_KEY_ROTATION_DISABLED

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_kms_key"):
                if report := _kms_key_is_key_rotation_absent_or_disabled(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=(
            "src.lib_path.f396.tfm_kms_key_is_key_rotation_absent_or_disabled"
        ),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
