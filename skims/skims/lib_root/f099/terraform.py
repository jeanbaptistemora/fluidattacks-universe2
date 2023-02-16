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


def _unencrypted_buckets(graph: Graph, nid: NId) -> Iterator[NId]:
    if not get_argument(graph, nid, "server_side_encryption_configuration"):
        has_sse_config: bool = False
        for sse_config in iterate_resource(
            graph, "aws_s3_bucket_server_side_encryption_configuration"
        ):
            sse_config_name = get_attribute(graph, sse_config, "bucket")
            b_name = get_attribute(graph, nid, "bucket")
            b_tf_reference = graph.nodes[nid].get("tf_reference")
            if sse_config_name[1] in (b_name[1], f"{b_tf_reference}.id"):
                has_sse_config = True
                break
        if not has_sse_config:
            yield nid


def tfm_unencrypted_buckets(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_UNENCRYPTED_BUCKETS

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_s3_bucket"):
                for report in _unencrypted_buckets(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f099.unencrypted_buckets",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
