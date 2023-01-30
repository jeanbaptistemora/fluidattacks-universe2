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


def _ec2_instances_without_profile(graph: Graph, nid: NId) -> Optional[NId]:
    expected_attr = "iam_instance_profile"
    is_vuln = True
    for c_id in adj_ast(graph, nid, label_type="Pair"):
        key_id = graph.nodes[c_id]["key_id"]
        key = graph.nodes[key_id]["value"]
        if key == expected_attr:
            is_vuln = False
    if is_vuln:
        return nid
    return None


def tfm_ec2_instances_without_profile(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_INST_WITHOUT_PROFILE

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_instance"):
                if report := _ec2_instances_without_profile(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f024_aws.instances_without_profile",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
