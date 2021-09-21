from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils import (
    graph as g,
)


def switch_without_default(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            for switch_id in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(label_type="switch_statement"),
            ):
                if not g.filter_nodes(
                    shard.graph,
                    nodes=g.adj_cfg(shard.graph, switch_id, depth=1),
                    predicate=g.pred_has_labels(
                        label_type="default_switch_label"
                    ),
                ):
                    yield shard, switch_id

    return get_vulnerabilities_from_n_ids(
        cwe=("478",),
        desc_key="src.lib_path.f073.switch_no_default",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F073
