from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from typing import (
    Set,
)
from utils import (
    graph as g,
)


def insecure_exceptions(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        bad: Set[str] = {"Exception"}
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.PHP,
        ):
            for catch_clause_id in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(label_type="catch_clause"),
            ):
                catch_clause = shard.graph.nodes[catch_clause_id]
                type_list_id = catch_clause["label_field_type"]

                for exc_type_id in g.filter_nodes(
                    shard.graph,
                    nodes=g.adj_ast(shard.graph, type_list_id),
                    predicate=g.pred_has_labels(label_type="named_type"),
                ):
                    if shard.graph.nodes[exc_type_id]["label_text"] in bad:
                        yield shard, exc_type_id

    return get_vulnerabilities_from_n_ids(
        cwe=("396",),
        desc_key="src.lib_path.f060.insecure_exceptions.description",
        desc_params=dict(lang="PHP"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F060
