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
    method = MethodsEnum.JAVA_INSECURE_AUTHENTICATION
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def insecure_authentication(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_INSECURE_AUTHENTICATION
    insecure_methods = {"setBasicAuth"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.filter_nodes(
                graph,
                graph.nodes,
                g.pred_has_labels(label_type="MethodInvocation"),
            ):
                expr = graph.nodes[n_id].get("expression")
                if expr in insecure_methods and get_eval_danger(graph, n_id):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f015.java_insecure_authentication",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )