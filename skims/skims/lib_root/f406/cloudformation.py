from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
)
from lib_path.common import (
    TRUE_OPTIONS,
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


def _aws_efs_unencrypted(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    encrypted, encrypted_val, encrypted_id = get_attribute(
        graph, val_id, "Encrypted"
    )
    if not encrypted:
        yield prop_id
    elif encrypted_val not in TRUE_OPTIONS:
        yield encrypted_id


def cfn_aws_efs_unencrypted(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_AWS_EFS_UNENCRYPTED

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "AWS::EFS::FileSystem"):
                for report in _aws_efs_unencrypted(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f406.aws_efs_unencrypted",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
