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
    Tuple,
)
import utils.graph as g


def split_function_name(f_names: str) -> Tuple[str, str]:
    name_l = f_names.split(".")
    if len(name_l) < 2:
        return "", name_l[-1]
    return name_l[-2], name_l[-1]


def get_eval_danger(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def ts_insecure_ciphers(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TS_INSECURE_CIPHERS
    danger_algos = {"DES", "RC4", "RSA"}
    danger_m = {"encrypt", "decrypt"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.TYPESCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="MethodInvocation"),
            ):
                f_name = graph.nodes[n_id]["expression"]
                algo, crypt = split_function_name(f_name)
                if algo in danger_algos and crypt in danger_m:
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def ts_insecure_aes_cipher(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TS_INSECURE_AES_CIPHER
    crypto_algo = {"AES"}
    danger_m = {"encrypt", "decrypt"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.TYPESCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="MethodInvocation"),
            ):
                f_name = graph.nodes[n_id]["expression"]
                algo, crypt = split_function_name(f_name)
                if (
                    algo in crypto_algo
                    and crypt in danger_m
                    and (al_id := graph.nodes[n_id].get("arguments_id"))
                    and len(g.adj_ast(graph, al_id)) > 2
                    and get_eval_danger(
                        graph, g.adj_ast(graph, al_id)[2], method
                    )
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
