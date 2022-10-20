# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
)
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
    method = MethodsEnum.CS_OPEN_REDIRECT
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def open_redirect(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for member in yield_syntax_graph_member_access(
                graph, {"Response"}
            ):
                pred = g.pred_ast(graph, member)[0]
                if graph.nodes[member].get(
                    "member"
                ) == "Redirect" and get_eval_danger(graph, pred):
                    yield shard, pred

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f063.c_sharp_open_redirect",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_OPEN_REDIRECT,
    )
