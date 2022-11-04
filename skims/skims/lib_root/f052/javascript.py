# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from contextlib import (
    suppress,
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
    Iterator,
    Tuple,
)
from utils.crypto import (
    insecure_elliptic_curve as eval_elliptic_curve,
)
import utils.graph as g
from utils.string import (
    complete_attrs_on_set,
)


def split_function_name(f_names: str) -> Tuple[str, str]:
    name_l = f_names.lower().split(".")
    if len(name_l) < 2:
        return "", name_l[-1]
    return name_l[-2], name_l[-1]


def get_eval_danger(graph: Graph, n_id: str, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def get_node_values(
    graph: Graph, n_id: str, method: MethodsEnum
) -> Iterator[str]:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.triggers != set():
            yield "".join(list(evaluation.triggers))


def is_insecure_encrypt(
    graph: Graph, al_id: NId, algo: str, method: MethodsEnum
) -> bool:
    if algo in {"des", "rc4", "rsa"}:
        return True
    if (args := g.adj_ast(graph, al_id)) and len(args) > 2:
        return get_eval_danger(graph, args[2], method)
    return False


def eval_insecure_curve(
    graph: Graph, obj_id: NId, method: MethodsEnum
) -> bool:
    for curve_value in get_node_values(graph, obj_id, method):
        if eval_elliptic_curve(curve_value):
            return True
    return False


def eval_insecure_options(
    graph: Graph, algo_id: NId, options_id: NId, method: MethodsEnum
) -> bool:
    algo_values = get_node_values(graph, algo_id, method)
    key_values = get_node_values(graph, options_id, method)
    for algo in algo_values:
        for key in key_values:
            if algo.lower() == "rsa":
                with suppress(ValueError):
                    value = int(key)
                    if value < 2048:
                        return True
            if algo.lower() == "ec" and eval_elliptic_curve(key):
                return True
    return False


def javascript_insecure_hash(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_INSECURE_HASH
    danger_methods = complete_attrs_on_set({"crypto.createHash"})

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="MethodInvocation"),
            ):
                if (
                    graph.nodes[n_id]["expression"] in danger_methods
                    and (al_id := graph.nodes[n_id].get("arguments_id"))
                    and (test_node := g.match_ast(graph, al_id).get("__0__"))
                    and get_eval_danger(graph, test_node, method)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def javascript_insecure_create_cipher(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_INSECURE_CREATE_CIPHER
    ciphers_methods = {
        "createdecipher",
        "createcipher",
        "createdecipheriv",
        "createcipheriv",
    }

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVASCRIPT,
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
                _, crypt = split_function_name(f_name)
                if (
                    crypt in ciphers_methods
                    and (al_id := graph.nodes[n_id].get("arguments_id"))
                    and (args := g.adj_ast(graph, al_id))
                    and len(args) > 0
                    and get_eval_danger(graph, args[0], method)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def javascript_insecure_encrypt(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_INSECURE_ENCRYPT
    crypto_methods = {"encrypt", "decrypt"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVASCRIPT,
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
                    crypt in crypto_methods
                    and (al_id := graph.nodes[n_id].get("arguments_id"))
                    and is_insecure_encrypt(graph, al_id, algo, method)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def javascript_insecure_ecdh_key(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_INSECURE_KEY
    danger_f = {"createecdh"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVASCRIPT,
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
                _, key = split_function_name(f_name)
                if (
                    key in danger_f
                    and (al_id := graph.nodes[n_id].get("arguments_id"))
                    and (args := g.adj_ast(graph, al_id))
                    and len(args) > 0
                    and eval_insecure_curve(graph, args[0], method)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JS_INSECURE_KEY,
    )


def javascript_insecure_key_pair(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_INSECURE_KEY
    danger_f = {"generatekeypair"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVASCRIPT,
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
                _, key = split_function_name(f_name)
                if (
                    key in danger_f
                    and (al_id := graph.nodes[n_id].get("arguments_id"))
                    and (args := g.adj_ast(graph, al_id))
                    and len(args) > 1
                    and eval_insecure_options(graph, args[0], args[1], method)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
