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


def _elb2_uses_insecure_protocol(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    protocol, protocol_val, protocol_id = get_attribute(
        graph, val_id, "Protocol"
    )
    target, target_val, _ = get_attribute(graph, val_id, "TargetType")
    is_secure = False
    if not (
        (protocol and protocol_val != "HTTP")
        or (target and target_val == "lambda")
    ):
        yield protocol_id
    else:
        is_secure = True
    if not protocol and not is_secure:
        yield prop_id


def cfn_elb2_uses_insecure_protocol(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_ELB2_INSEC_PROTO

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(
                graph, "AWS::ElasticLoadBalancingV2::TargetGroup"
            ):
                for report in _elb2_uses_insecure_protocol(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f372.elb2_uses_insecure_protocol",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
