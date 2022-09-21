# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.utilities.c_sharp import (
    get_first_member_syntax_graph,
)
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
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
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
    get_object_identifiers,
)


def remote_command_execution(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_REMOTE_COMMAND_EXECUTION
    c_sharp = GraphLanguage.CSHARP
    danger_params = {"HttpRequest", "UserParams"}

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue

            graph = shard.syntax_graph
            executors_objs = get_object_identifiers(graph, {"Executor"})

            executors = list(
                search_method_invocation_naive(graph, {"Execute"})
            )
            danger_meths = set(
                search_method_invocation_naive(graph, {"Start"})
            )
            methods = [
                executor
                if (
                    (member := get_first_member_syntax_graph(graph, executor))
                    and graph.nodes[member].get("symbol") in executors_objs
                )
                else None
                for executor in executors
            ]
            danger_meths.update(filter(None, methods))
            for n_id in danger_meths:
                for path in get_backward_paths(graph, n_id):
                    evaluation = evaluate(method, graph, path, n_id)
                    if evaluation and evaluation.triggers == danger_params:
                        yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f004.remote_command_execution",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
