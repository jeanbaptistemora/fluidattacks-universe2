from lib_root.utilities.json import (
    get_value,
)
from lib_root.utilities.terraform import (
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


def _public_buckets(graph: Graph, nid: NId) -> Optional[NId]:
    expected_attr = "acl"
    for c_id in adj_ast(graph, nid, label_type="Pair"):
        key_id = graph.nodes[c_id]["key_id"]
        key = graph.nodes[key_id]["value"]
        value_id = graph.nodes[c_id]["value_id"]
        value = get_value(graph, value_id)
        if key == expected_attr and value == "public-read-write":
            return value_id
    return None


def tfm_public_buckets(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_PUBLIC_BUCKETS

    def n_ids() -> Iterable[GraphShardNode]:
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
