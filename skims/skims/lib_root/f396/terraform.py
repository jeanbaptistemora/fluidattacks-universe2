from collections.abc import (
    Iterator,
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


def _kms_key_is_key_rotation_absent_or_disabled(
    graph: Graph, nid: NId
) -> NId | None:
    en_key_rot, en_key_rot_val, en_key_rot_id = get_attribute(
        graph, nid, "enable_key_rotation"
    )
    key_spec, key_spec_val, _ = get_attribute(
        graph, nid, "customer_master_key_spec"
    )
    if key_spec and key_spec_val != "SYMMETRIC_DEFAULT":
        return None
    if not en_key_rot:
        return nid
    if en_key_rot_val in {"false", "0"}:
        return en_key_rot_id
    return None


def tfm_kms_key_is_key_rotation_absent_or_disabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_KMS_KEY_ROTATION_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
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
