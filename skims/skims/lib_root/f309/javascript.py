# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
)
from model.graph_model import (
    Graph,
    GraphDB,
    GraphShardMetadataLanguage,
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
    filter_ast,
    get_backward_paths,
)
from typing import (
    Iterable,
)
from utils import (
    graph as g,
)


def is_filter_insecure(
    graph: Graph,
    n_id: NId,
    method: core_model.MethodsEnum,
) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def has_algorithm_insecure(
    graph: Graph,
    n_id: NId,
    method: core_model.MethodsEnum,
) -> bool:
    attrs = {"algorithm", "algorithms"}
    if args_id := graph.nodes[g.pred(graph, n_id)[0]].get("arguments_id"):
        for node in filter_ast(graph, args_id, {"SymbolLookup"}):
            if graph.nodes[node]["symbol"] in attrs and (
                (
                    test_id := g.match_ast(graph, g.pred(graph, node)[0]).get(
                        "__1__"
                    )
                )
                and is_filter_insecure(graph, test_id, method)
            ):
                return True
    return False


def uses_insecure_jwt_token(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.JS_INSECURE_JWT_TOKEN
    jwt_methods = {"sign", "verify"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in yield_syntax_graph_member_access(graph, jwt_methods):
                if has_algorithm_insecure(graph, nid, method):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f309.js_uses_insecure_jwt_token",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
