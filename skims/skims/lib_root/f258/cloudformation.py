from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
)
from lib_path.common import (
    FALSE_OPTIONS,
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


def _elb2_has_not_deletion_protection(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    load_balancer, _, load_id = get_attribute(
        graph, val_id, "LoadBalancerAttributes"
    )
    if not load_balancer:
        yield prop_id
    else:
        key_exist = False
        load_attrs = graph.nodes[load_id]["value_id"]
        for c_id in adj_ast(graph, load_attrs):
            key, key_val, _ = get_attribute(graph, c_id, "Key")
            if key and key_val == "deletion_protection.enabled":
                key_exist = True
                _, value, value_id = get_attribute(graph, c_id, "Value")
                if value in FALSE_OPTIONS:
                    yield value_id
        if not key_exist:
            yield load_id


def cfn_elb2_has_not_deletion_protection(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_ELB2_NOT_DELETION_PROTEC

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(
                graph, "AWS::ElasticLoadBalancingV2::LoadBalancer"
            ):
                for report in _elb2_has_not_deletion_protection(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=("src.lib_path.f258.elb2_has_not_deletion_protection"),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
