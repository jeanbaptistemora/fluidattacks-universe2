# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_sast.types import (
    ShardDb,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    Graph,
    GraphDB,
    GraphShardMetadataLanguage,
    GraphShardNodes,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
import utils.graph as g


def get_eval_danger(graph: Graph, n_id: str, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        if (
            evaluation := evaluate(method, graph, path, n_id)
        ) and evaluation.triggers == {"Random"}:
            return True
    return False


def weak_random(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_WEAK_RANDOM

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="CallExpression"),
            ):
                if "cookie" not in graph.nodes[n_id]["function_name"]:
                    continue

                if (
                    (al_id := graph.nodes[n_id]["arguments_id"])
                    and (test_node := g.match_ast(graph, al_id).get("__1__"))
                    and get_eval_danger(graph, test_node, method)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f034.javascript_insecure_randoms.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
