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
    Optional,
    Tuple,
)
from utils.crypto import (
    insecure_elliptic_curve as eval_elliptic_curve,
)
import utils.graph as g
from utils.languages.javascript import (
    is_cipher_vulnerable as eval_cipher_value,
)
from utils.string import (
    complete_attrs_on_set,
)


def split_function_name(f_names: str) -> Tuple[str, str]:
    name_l = f_names.split(".")
    if len(name_l) < 2:
        return "", name_l[-1]
    return name_l[-2], name_l[-1]


def eval_cipher_config(alg: str, mode: str, pad: Optional[str] = None) -> bool:
    pad = pad or ""
    alg = alg.lower()
    mode = mode.lower()
    pad = pad.lower()
    return any(
        (
            alg == "aes" and mode == "ecb",
            alg == "aes" and mode == "ofb",
            alg == "aes" and mode == "cfb",
            alg == "aes" and mode == "cbc",
            alg == "rsa" and "oaep" not in pad,
        )
    )


def get_eval_danger(graph: Graph, n_id: str, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        if (
            evaluation := evaluate(method, graph, path, n_id)
        ) and evaluation.danger:
            return True
    return False


def get_node_values(
    graph: Graph, n_id: str, method: MethodsEnum
) -> Iterator[str]:
    for path in get_backward_paths(graph, n_id):
        if (
            evaluation := evaluate(method, graph, path, n_id)
        ) and evaluation.triggers != set():
            yield "".join(list(evaluation.triggers))


def eval_insecure_cipher(graph: Graph, n_id: NId) -> bool:
    method = MethodsEnum.JS_INSECURE_CIPHER
    for cipher_val in get_node_values(graph, n_id, method):
        if eval_cipher_value(cipher_val):
            return True
    return False


def analyze_crypto_config(
    algo: str,
    mode_values: Iterator[str],
    pad_values: Optional[Iterator[str]],
) -> bool:
    for mode in mode_values:
        if pad_values:
            for pad in pad_values:
                if eval_cipher_config(algo, mode, pad):
                    return True
        else:
            if eval_cipher_config(algo, mode, None):
                return True

    return False


def eval_insecure_crypto(graph: Graph, obj_id: NId, algorithm: str) -> bool:
    method = MethodsEnum.JS_INSECURE_CIPHER
    algo = algorithm.lower()
    mode_values = None
    pad_values = None
    for pair_id in g.match_ast_group_d(graph, obj_id, "Pair"):
        pair_node = graph.nodes[pair_id]
        key = pair_node["key_id"]
        value = pair_node["value_id"]
        if graph.nodes[key].get("symbol") == "mode":
            mode_values = get_node_values(graph, value, method)
        if graph.nodes[key].get("symbol") == "padding":
            pad_values = get_node_values(graph, value, method)

    if algo == "aes" and not mode_values:
        return True

    if not mode_values:
        return False

    return analyze_crypto_config(algo, mode_values, pad_values)


def is_insecure_cipher(graph: Graph, n_id: NId) -> bool:
    native_ciphers = {"createCipheriv", "createDecipheriv"}
    crypto1 = {"DES", "RC4"}
    crypto2 = {"AES", "RSA"}

    n_attrs = graph.nodes[n_id]

    al_id = n_attrs.get("arguments_id")
    if not al_id:
        return False
    call_al = g.match_ast(graph, al_id)

    f_name = n_attrs["expression"]
    algo, crypt = split_function_name(f_name)
    is_insecure = False
    if crypt in native_ciphers and (test_node := call_al.get("__0__")):
        is_insecure = eval_insecure_cipher(graph, test_node)
    elif algo in crypto1 and crypt == "encrypt":
        is_insecure = True
    elif (
        algo in crypto2
        and crypt == "encrypt"
        and (test_node := call_al.get("__2__"))
    ):
        is_insecure = eval_insecure_crypto(graph, test_node, algo)

    return is_insecure


def eval_insecure_key(algo: str, key: str) -> bool:
    algo = algo.lower()
    if algo == "rsa":
        with suppress(ValueError):
            value = int(key)
        return value < 2048
    if algo == "ec":
        return eval_elliptic_curve(key)
    return False


def eval_insecure_curve(graph: Graph, obj_id: NId) -> bool:
    method = MethodsEnum.JS_INSECURE_KEY
    for curve_value in get_node_values(graph, obj_id, method):
        if eval_elliptic_curve(curve_value):
            return True
    return False


def eval_insecure_options(graph: Graph, algo_id: NId, options_id: NId) -> bool:
    method = MethodsEnum.JS_INSECURE_KEY
    algo_values = get_node_values(graph, algo_id, method)
    key_values = get_node_values(graph, options_id, method)

    for algo in algo_values:
        for key in key_values:
            if eval_insecure_key(algo, key):
                return True

    return False


def is_insecure_key(graph: Graph, n_id: NId) -> bool:
    function1 = {"createECDH"}
    function2 = {"generateKeyPair"}
    n_attrs = graph.nodes[n_id]
    al_id = n_attrs.get("arguments_id")
    if not al_id:
        return False
    call_al = g.match_ast(graph, al_id)
    algo_node = call_al.get("__0__")
    opt_node = call_al.get("__1__")

    f_name = n_attrs["expression"]
    _, key = split_function_name(f_name)

    if key in function1 and algo_node:
        return eval_insecure_curve(graph, algo_node)

    if key in function2 and algo_node and opt_node:
        return eval_insecure_options(graph, algo_node, opt_node)

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


def javascript_insecure_cipher(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_INSECURE_CIPHER

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
                if is_insecure_cipher(graph, n_id):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def javascript_insecure_key(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
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
                if is_insecure_key(graph, n_id):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JS_INSECURE_KEY,
    )
