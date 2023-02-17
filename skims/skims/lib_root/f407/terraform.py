from collections.abc import (
    Iterator,
)
from lib_root.utilities.terraform import (
    get_argument,
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


def _aws_ebs_volumes_unencrypted(graph: Graph, nid: NId) -> NId | None:
    if root := get_argument(graph, nid, "root_block_device"):
        attr, attr_val, attr_id = get_attribute(graph, root, "encrypted")
        if not attr:
            return root
        if attr_val.lower() == "false":
            return attr_id
    else:
        return nid
    return None


def tfm_aws_ebs_volumes_unencrypted(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AWS_EBS_VOLUMES_UNENCRYPTED

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_launch_configuration"):
                if report := _aws_ebs_volumes_unencrypted(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f407.tfm_aws_ebs_volumes_unencrypted",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
