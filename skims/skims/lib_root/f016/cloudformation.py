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


def _elb_without_sslpolicy(graph: Graph, nid: NId) -> Iterator[NId]:
    if not get_attribute(graph, nid, "SslPolicy")[0]:
        yield nid


def cfn_elb_without_sslpolicy(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_ELB_WITHOUT_SSLPOLICY

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.YAML):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(
                graph, "AWS::ElasticLoadBalancingV2::Listener"
            ):
                for report in _elb_without_sslpolicy(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f016.aws_elb_without_sslpolicy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
