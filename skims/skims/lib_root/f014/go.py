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


def float_currency(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        def _predicate(n_id: str) -> bool:
            return g.pred_has_labels(label_type="assignment_statement")(
                n_id
            ) or g.pred_has_labels(label_type="short_var_declaration")(n_id)

        smells: Set[str] = {
            "amount",
            "cash",
            "cost",
            "orden",
            "order",
            "precio",
            "price",
            "valor",
            "value",
        }
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.GO,
        ):
            graph = shard.graph
            for assignment in g.filter_nodes(
                graph, graph.nodes, predicate=_predicate
            ):
                c_ids = g.get_ast_childs(graph, assignment, "expression_list")
                vars_ids = g.get_ast_childs(graph, c_ids[0], "identifier")
                func_id = g.get_ast_childs(graph, c_ids[1], "call_expression")
                if (
                    func_id
                    and vars_ids
                    and "F109"
                    in graph.nodes[func_id[0]].get("label_input_type", {})
                    and any(
                        smell in graph.nodes[vars_ids[0]]["label_text"].lower()
                        for smell in smells
                    )
                ):
                    yield shard, assignment

    return get_vulnerabilities_from_n_ids(
        cwe=("197",),
        desc_key="F109.description",
        desc_params={},
        finding=core_model.FindingEnum.F109,
        graph_shard_nodes=n_ids(),
    )
