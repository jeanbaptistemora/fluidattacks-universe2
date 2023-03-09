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


def _instances_without_profile(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    instance_profile, _, _ = get_attribute(graph, val_id, "IamInstanceProfile")
    if not instance_profile:
        yield prop_id


def _groups_without_egress(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    egress, _, _ = get_attribute(graph, val_id, "SecurityGroupEgress")
    if not egress:
        yield prop_id


def cfn_groups_without_egress(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_GROUPS_WITHOUT_EGRESS

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "AWS::EC2::SecurityGroup"):
                for report in _groups_without_egress(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f024_aws.security_group_without_egress",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_instances_without_profile(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_INST_WITHOUT_PROFILE

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "AWS::EC2::Instance"):
                for report in _instances_without_profile(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f024_aws.instances_without_profile",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
