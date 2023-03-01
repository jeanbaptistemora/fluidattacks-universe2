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


def _ec2_use_default_security_group(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    launch_data, _, launch_data_id = get_attribute(
        graph, val_id, "LaunchTemplateData"
    )
    data_id = val_id
    report_id = prop_id
    if launch_data:
        data_id = graph.nodes[launch_data_id]["value_id"]
        report_id = launch_data_id
    if not (
        get_attribute(graph, data_id, "SecurityGroups")[0]
        or get_attribute(graph, data_id, "SecurityGroupIds")[0]
    ):
        yield report_id


def cfn_ec2_use_default_security_group(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_EC2_DEFAULT_SEC_GROUP

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in chain(
                iterate_resource(graph, "AWS::EC2::LaunchTemplate"),
                iterate_resource(graph, "AWS::EC2::Instance"),
            ):
                for report in _ec2_use_default_security_group(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f177.ec2_using_default_security_group",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
