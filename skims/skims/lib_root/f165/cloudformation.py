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


def _iam_is_policy_applying_to_users(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    user, _, _ = get_attribute(graph, val_id, "Users")
    if user:
        yield prop_id


def cfn_iam_is_policy_applying_to_users(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_PERMISSIONS_POLICY_APLLY_USERS

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in chain(
            graph_db.shards_by_language(GraphLanguage.YAML),
            graph_db.shards_by_language(GraphLanguage.JSON),
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in chain(
                iterate_resource(graph, "AWS::IAM::ManagedPolicy"),
                iterate_resource(graph, "AWS::IAM::Policy"),
            ):
                for report in _iam_is_policy_applying_to_users(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f165.iam_policies_applying_to_users",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
