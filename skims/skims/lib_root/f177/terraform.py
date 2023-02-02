from itertools import (
    chain,
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

SECURITY_GROUP_ATTRIBUTES = {"security_groups", "vpc_security_group_ids"}


def _use_default_security_group(graph: Graph, nid: NId) -> Optional[NId]:
    has_attr = False
    for b_id in adj_ast(graph, nid, label_type="Pair"):
        key_id = graph.nodes[b_id]["key_id"]
        key = graph.nodes[key_id]["value"]
        if key in SECURITY_GROUP_ATTRIBUTES:
            has_attr = True
    if not has_attr:
        return nid
    return None


def ec2_use_default_security_group(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.EC2_DEFAULT_SEC_GROUP

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in chain(
                iterate_resource(graph, "aws_instance"),
                iterate_resource(graph, "aws_launch_template"),
            ):
                if report := _use_default_security_group(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f177.ec2_using_default_security_group",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
