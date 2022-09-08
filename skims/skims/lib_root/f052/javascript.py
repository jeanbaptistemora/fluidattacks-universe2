# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from itertools import (
    chain,
)
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
    GraphShard,
    GraphShardMetadataLanguage,
    GraphShardNodes,
    SyntaxStepMethodInvocation,
    SyntaxSteps,
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
)
from utils.crypto import (
    insecure_elliptic_curve,
)
import utils.graph as g
from utils.languages.javascript import (
    is_cipher_vulnerable as javascript_cipher_vulnerable,
)
from utils.string import (
    build_attr_paths,
    complete_attrs_on_set,
    split_on_first_dot,
    split_on_last_dot,
)


def is_insecure_hash_argument(graph: Graph, param: str) -> bool:
    method = MethodsEnum.JS_INSECURE_HASH
    for path in get_backward_paths(graph, param):
        if evaluation := evaluate(method, graph, path, param):
            return evaluation.danger
    return False


def _test_native_cipher(
    # pylint: disable=too-many-arguments
    shard_db: ShardDb,
    graph_db: GraphDB,
    shard: GraphShard,
    syntax_steps: SyntaxSteps,
    step_index: int,
    invocation_step: SyntaxStepMethodInvocation,
) -> Iterator[Vulnerability]:
    method = MethodsEnum.JS_INSECURE_CIPHER
    finding = method.value.finding

    _, method_name = split_on_last_dot(invocation_step.method)
    if method_name not in {"createCipheriv", "createDecipheriv"}:
        return
    dependencies = get_dependencies(step_index, syntax_steps)
    algorithm = dependencies[-1]
    if (
        algorithm.type == "SyntaxStepLiteral"
        and (algorithm_value := algorithm.value)
        and javascript_cipher_vulnerable(algorithm_value)
    ):
        yield from get_vulnerabilities_from_n_ids(
            desc_key=("src.lib_path.f052.insecure_cipher.description"),
            desc_params=dict(lang="JavaScript"),
            graph_shard_nodes=[(shard, invocation_step.meta.n_id)],
            method=method,
        )
    elif algorithm.type == "SyntaxStepSymbolLookup":
        append_label_input(shard.graph, "1", finding)
        mark_methods_sink(
            finding,
            shard.graph,
            shard.syntax,
            {"createCipheriv", "createDecipheriv"},
        )
        yield from shard_n_id_query(
            shard_db,
            graph_db,
            shard,
            n_id="1",
            method=method,
        )
    else:
        return


def _test_crypto_js(
    shard_db: ShardDb,
    graph_db: GraphDB,
    shard: GraphShard,
    invocation_step: SyntaxStepMethodInvocation,
) -> Iterator[Vulnerability]:
    method = MethodsEnum.JS_INSECURE_CIPHER
    finding = method.value.finding

    _methods = [
        ("crypto-js", "DES.encrypt"),
        ("crypto-js", "RC4.encrypt"),
    ]
    methods = set(chain.from_iterable(build_attr_paths(*m) for m in _methods))
    _, method_name = split_on_first_dot(invocation_step.method)
    if method_name in methods:
        yield from get_vulnerabilities_from_n_ids(
            desc_key=("src.lib_path.f052.insecure_cipher.description"),
            desc_params=dict(lang="JavaScript"),
            graph_shard_nodes=[(shard, invocation_step.meta.n_id)],
            method=method,
        )
    elif method_name in complete_attrs_on_set(
        {
            "crypto-js.AES.encrypt",
            "crypto-js.RSA.encrypt",
        }
    ):
        append_label_input(shard.graph, "1", finding)
        mark_methods_sink(
            finding,
            shard.graph,
            shard.syntax,
            {"encrypt"},
        )
        yield from shard_n_id_query(
            shard_db,
            graph_db,
            shard,
            n_id="1",
            method=method,
        )


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
    shard_db: ShardDb,
    graph_db: GraphDB,
) -> Vulnerabilities:
    def find_vulns() -> Iterator[Vulnerability]:
        for (
            shard,
            syntax_steps,
            invocation_step,
            index,
        ) in yield_method_invocation(graph_db):
            yield from _test_native_cipher(
                shard_db,
                graph_db,
                shard,
                syntax_steps,
                index,
                invocation_step,
            )
            yield from _test_crypto_js(
                shard_db,
                graph_db,
                shard,
                invocation_step,
            )

    return tuple(find_vulns())


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
