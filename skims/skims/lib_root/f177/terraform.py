from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
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


def _use_default_security_group(graph: Graph, nid: NId) -> NId | None:
    sec_groups, _, _ = get_attribute(graph, nid, "security_groups")
    vpc_sec_groups, _, _ = get_attribute(graph, nid, "vpc_security_group_ids")
    if not (sec_groups or vpc_sec_groups):
        return nid
    return None


def ec2_use_default_security_group(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.EC2_DEFAULT_SEC_GROUP

    def n_ids() -> Iterator[GraphShardNode]:
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
