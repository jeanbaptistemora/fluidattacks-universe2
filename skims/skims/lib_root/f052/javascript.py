from itertools import (
    chain,
)
from lib_root.utilities.javascript import (
    yield_method_invocation,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
    Vulnerability,
)
from model.graph_model import (
    GraphDB,
    GraphShard,
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
from typing import (
    Iterator,
)
from utils.crypto import (
    insecure_elliptic_curve,
)
from utils.languages.javascript import (
    is_cipher_vulnerable as javascript_cipher_vulnerable,
)
from utils.string import (
    build_attr_paths,
    complete_attrs_on_set,
    split_on_first_dot,
    split_on_last_dot,
)


def _test_native_cipher(
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
        yield get_vulnerabilities_from_n_ids(
            cwe=("310", "327"),
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
        yield shard_n_id_query(
            graph_db,
            shard,
            n_id="1",
            method=method,
        )
    else:
        return


def _test_crypto_js(
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
        yield get_vulnerabilities_from_n_ids(
            cwe=("310", "327"),
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
        yield shard_n_id_query(
            graph_db,
            shard,
            n_id="1",
            method=method,
        )


def javascript_insecure_hash(graph_db: GraphDB) -> Vulnerabilities:
    def find_vulns() -> Iterator[Vulnerability]:
        for (
            shard,
            syntax_steps,
            invocation_step,
            index,
        ) in yield_method_invocation(graph_db):
            danger_methods = {"createHash"}
            var, method_name = split_on_last_dot(invocation_step.method)
            if method_name not in danger_methods and var not in danger_methods:
                continue

            dependencies = get_dependencies(index, syntax_steps)
            algorithm = dependencies[-1]
            if (
                algorithm.type == "SyntaxStepLiteral"
                and (algorithm_value := algorithm.value)
                and any(
                    alg in algorithm_value.lower()
                    for alg in (
                        "md2",
                        "md4",
                        "md5",
                        "sha1",
                        "sha-1",
                    )
                )
            ):
                yield get_vulnerabilities_from_n_ids(
                    cwe=("310", "327"),
                    desc_key=("src.lib_path.f052.insecure_cipher.description"),
                    desc_params=dict(lang="JavaScript"),
                    graph_shard_nodes=[(shard, invocation_step.meta.n_id)],
                    method=MethodsEnum.JS_INSECURE_HASH,
                )

    return tuple(chain.from_iterable(find_vulns()))


def javascript_insecure_cipher(
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
                graph_db,
                shard,
                syntax_steps,
                index,
                invocation_step,
            )
            yield from _test_crypto_js(graph_db, shard, invocation_step)

    return tuple(chain.from_iterable(find_vulns()))


def javascript_insecure_key(graph_db: GraphDB) -> Vulnerabilities:
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
                    yield get_vulnerabilities_from_n_ids(
                        cwe=("310", "327"),
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
                yield shard_n_id_query(
                    graph_db,
                    shard,
                    n_id="1",
                    method=method,
                )

    return tuple(chain.from_iterable(find_vulns()))
