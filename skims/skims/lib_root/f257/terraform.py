from collections.abc import (
    Iterator,
)
from lib_root.utilities.terraform import (
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


def _has_not_termination_protection(graph: Graph, nid: NId) -> NId | None:
    attr, attr_val, attr_id = get_attribute(
        graph, nid, "disable_api_termination"
    )
    if not attr:
        return nid
    if attr_val.lower() == "false":
        return attr_id
    return None


def tfm_ec2_has_not_termination_protection(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.EC2_NOT_TERMINATION_PROTEC

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.HCL):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in iterate_resource(graph, "aws_launch_template"):
                if report := _has_not_termination_protection(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f257.ec2_has_not_termination_protection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
