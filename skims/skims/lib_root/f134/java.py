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
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
    NId,
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
from typing import (
    Iterable,
)
from utils import (
    graph as g,
)


def get_eval_danger(graph: Graph, n_id: NId) -> bool:
    method = MethodsEnum.JAVA_INSECURE_CORS_ORIGIN
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def is_vulnerable_origin(graph: Graph, nid: NId, check: str) -> bool:
    arg_id = graph.nodes[nid].get("arguments_id")
    if not arg_id:
        return False

    childs = g.adj_ast(graph, arg_id)
    test_node = None
    if (
        check == "add"
        and len(childs) > 1
        and graph.nodes[childs[0]].get("value")
        == '"Access-Control-Allow-Origin"'
    ):
        test_node = childs[1]

    if check in {"allowedorigins", "addallowedorigin"} and len(childs) == 1:
        test_node = childs[0]

    if test_node:
        return get_eval_danger(graph, test_node)

    return False


def insecure_cors_origin(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_INSECURE_CORS_ORIGIN
    insecure_methods = {"add", "allowedorigins", "addallowedorigin"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in g.filter_nodes(
                graph,
                graph.nodes,
                g.pred_has_labels(label_type="MethodInvocation"),
            ):
                expr = graph.nodes[nid].get("expression")
                if (
                    expr
                    and expr.lower() in insecure_methods
                    and is_vulnerable_origin(graph, nid, expr.lower())
                ):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f134.cors_policy_allows_any_origin",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
