# Local libraries
from sast.query import get_vulnerabilities_from_n_ids
from utils import (
    graph as g,
)
from model import (
    core_model,
    graph_model,
)


def java_switch_without_default(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards:
            for switch_id in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(label_type="switch_statement"),
            ):
                if not g.filter_nodes(
                    shard.graph,
                    nodes=g.adj_ast(shard.graph, switch_id, depth=3),
                    predicate=g.pred_has_labels(label_type="default"),
                ):
                    yield shard, switch_id

    return get_vulnerabilities_from_n_ids(
        cwe=("478",),
        desc_key="src.lib_path.f073.switch_no_default",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


# Constants
FINDING: core_model.FindingEnum = core_model.FindingEnum.F073
QUERIES: graph_model.Queries = ((FINDING, java_switch_without_default),)
