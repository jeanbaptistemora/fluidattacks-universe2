from lib_root.utilities.terraform import (
    get_key_value,
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


def _ec2_monitoring_disabled(graph: Graph, nid: NId) -> Optional[NId]:
    expected_attr = "monitoring"
    has_attr = False
    for b_id in adj_ast(graph, nid, label_type="Pair"):
        key, value = get_key_value(graph, b_id)
        if key == expected_attr:
            has_attr = True
            if value.lower() in {"false", "0"}:
                return b_id
    if not has_attr:
        return nid
    return None


def tfm_ec2_monitoring_disabled(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_EC2_MONITORING_DISABLED

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_instance"):
                if report := _ec2_monitoring_disabled(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f400.has_monitoring_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
