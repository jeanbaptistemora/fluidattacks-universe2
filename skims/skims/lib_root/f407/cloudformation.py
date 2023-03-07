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
from utils.graph import (
    adj_ast,
)


def _aws_ebs_volumes_unencrypted(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    mappings, _, mappings_id = get_attribute(
        graph, val_id, "BlockDeviceMappings"
    )
    if mappings:
        mappings_attr = graph.nodes[mappings_id]["value_id"]
        for c_id in adj_ast(graph, mappings_attr):
            ebs, _, ebs_id = get_attribute(graph, c_id, "Ebs")
            if ebs:
                ebs_attrs = graph.nodes[ebs_id]["value_id"]
                encrypted, encrypted_val, encrypted_id = get_attribute(
                    graph, ebs_attrs, "Encrypted"
                )
            if not encrypted:
                yield ebs_id
            elif encrypted_val not in TRUE_OPTIONS:
                yield encrypted_id


def cfn_aws_ebs_volumes_unencrypted(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_AWS_EBS_VOLUMES_UNENCRYPTED

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(
                graph, "AWS::AutoScaling::LaunchConfiguration"
            ):
                for report in _aws_ebs_volumes_unencrypted(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f407.cfn_aws_ebs_volumes_unencrypted",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
