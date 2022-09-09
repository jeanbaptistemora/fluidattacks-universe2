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
    GraphShardNodes,
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
    List,
    Optional,
    Tuple,
)
from utils.crypto import (
    insecure_elliptic_curve,
    is_vulnerable_cipher,
)
import utils.graph as g
from utils.languages.javascript import (
    is_cipher_vulnerable as javascript_cipher_vulnerable,
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
        if evaluation := evaluate(method, graph, path, n_id):
            return evaluation.danger
    return False


def get_eval_triggers(
    graph: Graph, n_id: str, method: MethodsEnum
) -> List[str]:
    for path in get_backward_paths(graph, n_id):
        if evaluation := evaluate(method, graph, path, n_id):
            return list(evaluation.triggers)
    return [""]


def is_insecure_crypto(graph: Graph, obj_id: Optional[NId], algo: str) -> bool:
    if not obj_id or graph.nodes[obj_id]["label_type"] != "Object":
        return False
    method = MethodsEnum.JS_INSECURE_CIPHER
    algo = algo.lower()
    mode = ""
    padding = None
    obj_configs = g.match_ast_group_d(graph, obj_id, "Pair")
    for nid in obj_configs:
        key = graph.nodes[nid].get("key_id")
        key_identifier = graph.nodes[key].get("symbol").lower()
        test_node = graph.nodes[nid]["value_id"]
        if key_identifier == "mode":
            mode = "".join(get_eval_triggers(graph, test_node, method))
        elif key_identifier == "padding":
            padding = "".join(get_eval_triggers(graph, test_node, method))

    return is_vulnerable_cipher(algo, mode, padding)


def is_insecure_key(algo: str, key: str) -> bool:
    algo = algo.lower()
    if algo == "rsa":
        with suppress(ValueError):
            value = int(key)
        return value < 2048
    if algo == "ec":
        return insecure_elliptic_curve(key)
    return False


def javascript_insecure_hash(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_INSECURE_HASH
    danger_methods = complete_attrs_on_set({"crypto.createHash"})

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="CallExpression"),
            ):
                if graph.nodes[n_id]["function_name"] not in danger_methods:
                    continue

                if (
                    (
                        al_id := g.match_ast(graph, n_id, "ArgumentList").get(
                            "ArgumentList"
                        )
                    )
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
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_INSECURE_CIPHER
    native_ciphers = {"createCipheriv", "createDecipheriv"}
    crypto1 = {"DES", "RC4"}
    crypto2 = {"AES", "RSA"}

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="CallExpression"),
            ):
                f_name = graph.nodes[n_id]["function_name"]
                algo, crypt = split_function_name(f_name)
                al_id = g.match_ast(graph, n_id, "ArgumentList").get(
                    "ArgumentList"
                )
                if not al_id:
                    continue

                call_al = g.match_ast(graph, al_id)
                is_insecure = False
                if crypt in native_ciphers and (
                    test_node := call_al.get("__0__")
                ):
                    value = "".join(
                        get_eval_triggers(graph, test_node, method)
                    )
                    is_insecure = javascript_cipher_vulnerable(value)
                elif algo in crypto1 and crypt == "encrypt":
                    is_insecure = True
                elif algo in crypto2 and crypt == "encrypt":
                    test_node = call_al.get("__2__")
                    is_insecure = is_insecure_crypto(graph, test_node, algo)

                if is_insecure:
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def javascript_insecure_key(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_INSECURE_KEY
    function1 = {"createECDH"}
    function2 = {"generateKeyPair"}

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="CallExpression"),
            ):
                f_name = graph.nodes[n_id]["function_name"]
                _, key = split_function_name(f_name)
                al_id = g.match_ast(graph, n_id, "ArgumentList").get(
                    "ArgumentList"
                )
                if not al_id:
                    continue

                call_al = g.match_ast(graph, al_id)
                algo_node = call_al.get("__0__")
                options_node = call_al.get("__1__")
                is_insecure = False
                if key in function1 and algo_node:
                    value = "".join(
                        get_eval_triggers(graph, algo_node, method)
                    )
                    is_insecure = insecure_elliptic_curve(value)
                elif key in function2 and algo_node and options_node:
                    algo = "".join(get_eval_triggers(graph, algo_node, method))
                    key = "".join(
                        get_eval_triggers(graph, options_node, method)
                    )
                    is_insecure = is_insecure_key(algo, key)

                if is_insecure:
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JS_INSECURE_KEY,
    )
