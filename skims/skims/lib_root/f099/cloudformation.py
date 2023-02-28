from collections.abc import (
    Iterator,
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


def _unencrypted_buckets(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    bucket_encryption, _, _ = get_attribute(graph, val_id, "BucketEncryption")
    if not bucket_encryption:
        yield prop_id


def cfn_unencrypted_buckets(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_UNENCRYPTED_BUCKETS

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.YAML):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "AWS::S3::Bucket"):
                for report in _unencrypted_buckets(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f099.unencrypted_buckets",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
