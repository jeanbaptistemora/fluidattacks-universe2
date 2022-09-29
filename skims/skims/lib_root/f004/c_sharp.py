# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.utilities.common import (
    search_method_invocation_naive,
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


def is_execute_danger(graph: Graph, n_id: str, check: str) -> bool:
    method = MethodsEnum.CS_REMOTE_COMMAND_EXECUTION

    danger_p1 = {"UserConnection", "UserParams"}
    danger_p2 = {"Executor", "UserConnection", "UserParams"}

    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and (
            (check == "Start" and evaluation.triggers == danger_p1)
            or (check == "Execute" and evaluation.triggers == danger_p2)
        ):
            return True
    return False


def remote_command_execution(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in search_method_invocation_naive(graph, {"Start"}):
                if is_execute_danger(graph, n_id, "Start"):
                    yield shard, n_id

            for n_id in search_method_invocation_naive(graph, {"Execute"}):
                if is_execute_danger(graph, n_id, "Execute"):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f004.remote_command_execution",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_REMOTE_COMMAND_EXECUTION,
    )
