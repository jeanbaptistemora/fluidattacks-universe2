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
from typing import (
    Iterable,
)
from utils import (
    graph as g,
)


def is_argument_literal(graph: Graph, n_id: NId) -> bool:
    if (args := g.match_ast(graph, n_id)) and (
        len(args) == 1
        and graph.nodes[args.get("__0__")]["label_type"] == "Literal"
    ):
        return True
    return False


def uses_eval(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_USES_EVAL
    sensitive_methods = {"eval", "Function"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for member in g.filter_nodes(
                graph,
                graph.nodes,
                predicate=g.pred_has_labels(label_type="MethodInvocation"),
            ):
                if (args_id := graph.nodes[member].get("arguments_id")) and (
                    graph.nodes[member].get("expression") in sensitive_methods
                    and not is_argument_literal(graph, args_id)
                ):
                    yield shard, member

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f143.uses_eval",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
