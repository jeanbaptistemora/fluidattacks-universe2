from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
)
from lib_path.common import (
    FALSE_OPTIONS,
)
from lib_root.utilities.cloudformation import (
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
) -> Iterator[NId]:
    key_spec_symmetric = "SYMMETRIC_DEFAULT"
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    key_rot, key_rot_val, key_rot_id = get_attribute(
        graph, val_id, "EnableKeyRotation"
    )
    key_spec, key_spec_val, _ = get_attribute(graph, val_id, "KeySpec")
    if key_spec_val == key_spec_symmetric or key_spec is None:
        if not key_rot:
            yield prop_id
        elif key_rot_val in FALSE_OPTIONS:
            yield key_rot_id


def cfn_kms_key_is_key_rotation_absent_or_disabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_KMS_KEY_ROTATION_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "AWS::KMS::Key"):
                for report in _kms_key_is_key_rotation_absent_or_disabled(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=(
            "src.lib_path.f396.kms_key_is_key_rotation_absent_or_disabled"
        ),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
