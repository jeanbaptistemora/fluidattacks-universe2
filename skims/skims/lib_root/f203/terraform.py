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


def _public_buckets(graph: Graph, nid: NId) -> NId | None:
    attr, attr_val, attr_id = get_attribute(graph, nid, "acl")
    if attr and attr_val == "public-read-write":
        return attr_id
    return None


def tfm_public_buckets(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_PUBLIC_BUCKETS

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_s3_bucket"):
                if report := _public_buckets(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f203.public_buckets",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
