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


def get_eval_danger(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def is_validation_dangerous(
    graph: Graph, n_id: NId, method: MethodsEnum
) -> bool:
    parent_id = g.pred(graph, n_id)[0]
    if (
        graph.nodes[parent_id]["label_type"] == "Assignment"
        and (test_nid := g.adj_ast(graph, parent_id)[1])
        and get_eval_danger(graph, test_nid, method)
    ):
        return True
    return False


def insecure_certificate_validation(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    c_sharp = GraphLanguage.CSHARP
    method = MethodsEnum.CS_INSECURE_CERTIFICATE_VALIDATION
    danger_m = "ServerCertificateValidationCallback"

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in g.filter_nodes(
                graph,
                graph.nodes,
                g.pred_has_labels(label_type="MemberAccess"),
            ):
                if graph.nodes[nid].get(
                    "member"
                ) == danger_m and is_validation_dangerous(graph, nid, method):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f060.insecure_certificate_validation",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
