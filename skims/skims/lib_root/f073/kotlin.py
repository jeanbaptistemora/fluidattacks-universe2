from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from typing import (
    Tuple,
)
from utils import (
    graph as g,
)


def when_without_else(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.KOTLIN
        ):
            for when_id in g.filter_nodes(
                shard.graph,
                shard.graph.nodes,
                g.pred_has_labels(label_type="when_expression"),
            ):
                cases_ids = g.get_ast_childs(
                    shard.graph, when_id, "when_entry"
                )
                else_id: Tuple[str, ...] = tuple(
                    case_id
                    for case_id in cases_ids
                    if shard.graph.nodes[
                        str(
                            shard.graph.nodes[case_id][
                                "label_field_conditions"
                            ]
                        )
                    ]["label_type"]
                    == "when_entry_else"
                )
                empty_else: bool = False
                if else_id:
                    else_body = g.adj_ast(
                        shard.graph,
                        str(shard.graph.nodes[else_id[0]]["label_field_body"]),
                    )
                    empty_else = all(
                        shard.graph.nodes[n_id]["label_type"]
                        in {"{", "}", "comment"}
                        for n_id in else_body
                    )
                if not else_id or empty_else:
                    yield shard, when_id

    return get_vulnerabilities_from_n_ids(
        cwe=("478",),
        desc_key="src.lib_path.f073.when_no_else",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


# Constants
FINDING: core_model.FindingEnum = core_model.FindingEnum.F073
