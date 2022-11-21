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
    Optional,
)
from utils import (
    graph as g,
)


def has_cannonical_check(graph: Graph, symbol: str) -> Optional[NId]:
    for node in search_method_invocation_naive(graph, {"getCanonicalPath"}):
        if (
            graph.nodes[graph.nodes[node].get("object_id")].get("symbol")
            == symbol
        ):
            return g.pred(graph, node)[0]
    return None


def is_argument_safe(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    symbol = graph.nodes[n_id].get("symbol")
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if (
            evaluation
            and evaluation.triggers == {"ZipFile"}
            and (has_cannonical_check(graph, symbol) in path)
        ):
            return True
    return False


def zip_slip_injection(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_ZIP_SLIP_PATH_INJECTION
    read_entry = {"readFileToString"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in search_method_invocation_naive(graph, read_entry):
                if (args_id := graph.nodes[nid].get("arguments_id")) and (
                    (test_id := g.match_ast(graph, args_id).get("__0__"))
                    and not is_argument_safe(graph, test_id, method)
                ):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f063.zip_slip_path_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )