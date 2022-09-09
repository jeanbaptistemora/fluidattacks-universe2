# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.utilities.javascript import (
    yield_method_invocation,
)
from lib_sast.types import (
    ShardDb,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
    Vulnerability,
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
    shard_n_id_query,
)
from sast_syntax_readers.utils_generic import (
    get_dependencies,
)
from sast_transformations.danger_nodes.utils import (
    append_label_input,
    mark_methods_sink,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from typing import (
    Iterator,
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
    split_on_last_dot,
)


def is_insecure_hash_argument(graph: Graph, param: str) -> bool:
    method = MethodsEnum.JS_INSECURE_HASH
    for path in get_backward_paths(graph, param):
        if evaluation := evaluate(method, graph, path, param):
            return evaluation.danger
    return False


def is_insecure_native_cipher(graph: Graph, param: Optional[NId]) -> bool:
    method = MethodsEnum.JS_INSECURE_CIPHER
    if not param:
        return False

    for path in get_backward_paths(graph, param):
        if evaluation := evaluate(method, graph, path, param):
            eval_str = "".join(list(evaluation.triggers))
            return javascript_cipher_vulnerable(eval_str)
    return False


def get_obj_triggers(graph: Graph, pair: str) -> str:
    method = MethodsEnum.JS_INSECURE_CIPHER
    test_node = graph.nodes[pair]["value_id"]
    for path in get_backward_paths(graph, test_node):
        if evaluation := evaluate(method, graph, path, test_node):
            return "".join(list(evaluation.triggers))
    return ""


def is_insecure_crypto(graph: Graph, obj_id: Optional[NId], algo: str) -> bool:
    if not obj_id or graph.nodes[obj_id]["label_type"] != "Object":
        return False
    algo = algo.lower()
    mode = ""
    padding = None

    obj_configs = g.match_ast_group_d(graph, obj_id, "Pair")
    for nid in obj_configs:
        key = graph.nodes[nid].get("key_id")
        key_identifier = graph.nodes[key].get("symbol").lower()
        if key_identifier == "mode":
            mode = get_obj_triggers(graph, nid)
        elif key_identifier == "padding":
            padding = get_obj_triggers(graph, nid)

    return is_vulnerable_cipher(algo, mode, padding)


def _get_function_names(f_names: str) -> Tuple[str, str]:
    name_l = f_names.split(".")
    if len(name_l) < 2:
        return "", name_l[-1]
    return name_l[-2], name_l[-1]


def javascript_insecure_hash(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
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
                    and is_insecure_hash_argument(graph, test_node)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JS_INSECURE_HASH,
    )


def javascript_insecure_cipher(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
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
                algo, crypt = _get_function_names(f_name)
                al_id = g.match_ast(graph, n_id, "ArgumentList").get(
                    "ArgumentList"
                )
                if not al_id:
                    continue

                call_al = g.match_ast(graph, al_id)
                is_insecure = False
                if crypt in native_ciphers:
                    test_node = call_al.get("__0__")
                    is_insecure = is_insecure_native_cipher(graph, test_node)
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
        method=MethodsEnum.JS_INSECURE_CIPHER,
    )


def javascript_insecure_key(
    shard_db: ShardDb,
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_INSECURE_KEY
    finding = method.value.finding

    def find_vulns() -> Iterator[Vulnerability]:
        for (
            shard,
            syntax_steps,
            invocation_step,
            step_index,
        ) in yield_method_invocation(graph_db):
            _, method_name = split_on_last_dot(invocation_step.method)
            if method_name in {"createECDH"}:
                dependencies = get_dependencies(step_index, syntax_steps)
                curve = dependencies[-1]
                if (
                    curve.type == "SyntaxStepLiteral"
                    and (algorithm_value := curve.value)
                    and insecure_elliptic_curve(algorithm_value)
                ):
                    yield from get_vulnerabilities_from_n_ids(
                        desc_key="src.lib_path.f052.insecure_key.description",
                        desc_params=dict(lang="JavaScript"),
                        graph_shard_nodes=[(shard, invocation_step.meta.n_id)],
                        method=method,
                    )
            elif "generateKeyPair" in invocation_step.method:
                append_label_input(shard.graph, "1", finding)
                mark_methods_sink(
                    finding,
                    shard.graph,
                    shard.syntax,
                    {"generateKeyPair"},
                )
                yield from shard_n_id_query(
                    shard_db,
                    graph_db,
                    shard,
                    n_id="1",
                    method=method,
                )

    return tuple(find_vulns())
