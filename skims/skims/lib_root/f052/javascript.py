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
    List,
    Tuple,
)
from utils.crypto import (
    insecure_elliptic_curve as eval_elliptic_curve,
    is_vulnerable_cipher as eval_cipher_config,
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


def get_eval_danger(graph: Graph, n_id: str, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        if (
            evaluation := evaluate(method, graph, path, n_id)
        ) and evaluation.danger:
            return True
    return False


def get_eval_triggers(
    graph: Graph, n_id: str, method: MethodsEnum
) -> Iterator[List[str]]:
    for path in get_backward_paths(graph, n_id):
        if (
            evaluation := evaluate(method, graph, path, n_id)
        ) and evaluation.triggers != set():
            yield list(evaluation.triggers)


def eval_insecure_cipher(graph: Graph, obj_id: NId) -> bool:
    method = MethodsEnum.JS_INSECURE_CIPHER
    for triggers in get_eval_triggers(graph, obj_id, method):
        cipher_value = "".join(triggers)
        return eval_cipher_value(cipher_value)
    return False


def eval_insecure_crypto(graph: Graph, obj_id: NId, algo: str) -> bool:
    method = MethodsEnum.JS_INSECURE_CIPHER
    algo = algo.lower()
    mode = ""
    padding = None
    for triggers in get_eval_triggers(graph, obj_id, method):
        options = "".join(triggers).split(".")
        if "mode" in options and len(options) > options.index("mode"):
            mode = options[options.index("mode") + 1]
        if "padding" in options and len(options) > options.index("padding"):
            padding = options[options.index("padding") + 1]
        return eval_cipher_config(algo, mode, padding)

    return False


def is_insecure_cipher(graph: Graph, n_id: NId) -> bool:
    native_ciphers = {"createCipheriv", "createDecipheriv"}
    crypto1 = {"DES", "RC4"}
    crypto2 = {"AES", "RSA"}

    n_attrs = graph.nodes[n_id]
    f_name = n_attrs["expression"]
    algo, crypt = split_function_name(f_name)
    call_al = g.match_ast(graph, n_attrs["arguments_id"])
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
    for triggers in get_eval_triggers(graph, obj_id, method):
        curve_value = "".join(triggers)
        if eval_elliptic_curve(curve_value):
            return True
    return False


def eval_insecure_options(graph: Graph, algo_id: NId, options_id: NId) -> bool:
    method = MethodsEnum.JS_INSECURE_KEY
    for algo_trig in get_eval_triggers(graph, algo_id, method):
        algo = "".join(algo_trig)
        for opt_trig in get_eval_triggers(graph, options_id, method):
            key = "".join(opt_trig)
            if eval_insecure_key(algo, key):
                return True
    return False


def is_insecure_key(graph: Graph, n_id: NId) -> bool:
    function1 = {"createECDH"}
    function2 = {"generateKeyPair"}

    f_name = graph.nodes[n_id]["expression"]
    _, key = split_function_name(f_name)
    al_id = graph.nodes[n_id]["arguments_id"]

    call_al = g.match_ast(graph, al_id)
    algo_node = call_al.get("__0__")
    opt_node = call_al.get("__1__")

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
