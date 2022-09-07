# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.utilities.common import (
    search_method_invocation_naive,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
)
from model.graph_model import (
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


def insecure_logging(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.JAVA_INSECURE_LOGGING

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in search_method_invocation_naive(graph, {"info"}):
                if (
                    graph.nodes[graph.nodes[nid]["object_id"]].get("symbol")
                    != "Logger"
                ):
                    continue
                if test_node := graph.nodes[nid].get("arguments_id"):
                    for path in get_backward_paths(graph, test_node):
                        evaluation = evaluate(method, graph, path, test_node)
                        if (
                            evaluation
                            and evaluation.danger
                            and not (
                                "replaceAll" in evaluation.triggers
                                and "Sanitize" in evaluation.triggers
                            )
                        ):
                            yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.091.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
