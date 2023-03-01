from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
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


def _s3_bucket_versioning_disabled(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    version, _, version_id = get_attribute(
        graph, val_id, "VersioningConfiguration"
    )
    if version:
        data_id = graph.nodes[version_id]["value_id"]
        status, status_val, status_id = get_attribute(graph, data_id, "Status")
        if status is None:
            yield version_id
        elif status_val != "Enabled":
            yield status_id
    else:
        yield prop_id


def cfn_s3_bucket_versioning_disabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_S3_VERSIONING_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "AWS::S3::Bucket"):
                for report in _s3_bucket_versioning_disabled(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f335.cfn_s3_bucket_versioning_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
