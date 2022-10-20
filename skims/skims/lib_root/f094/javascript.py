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
    get_backward_paths,
)
from typing import (
    Iterable,
    Optional,
    Tuple,
)
from utils import (
    graph as g,
)


def eval_danger(
    graph: Graph,
    n_id: NId,
    method: core_model.MethodsEnum,
) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def get_mode_node(
    graph: Graph,
    members: Tuple[str, ...],
    identifier: str,
) -> Optional[NId]:
    test_id = None
    for member in members:
        if graph.nodes[member].get(identifier) == "mode":
            test_id = g.match_ast(graph, g.pred(graph, member)[0]).get("__1__")
    return test_id


def has_insecure_mode(
    graph: Graph,
    n_id: NId,
    method: core_model.MethodsEnum,
) -> bool:
    if nodes := g.get_ast_childs(graph, n_id, "SymbolLookup", depth=3):
        test_nid = get_mode_node(graph, nodes, "symbol")

    if not test_nid or eval_danger(graph, test_nid, method):
        return True
    return False


def uses_insecure_encrypt(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.JS_INSECURE_ENCRYPT
    encrypt = {"CryptoJS.AES.encrypt"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in search_method_invocation_naive(graph, encrypt):
                if (args_id := graph.nodes[nid].get("arguments_id")) and (
                    has_insecure_mode(graph, args_id, method)
                ):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f094.js_uses_insecure_encrypt",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
