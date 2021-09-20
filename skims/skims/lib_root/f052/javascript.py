from itertools import (
    chain,
)
from lib_root import (
    yield_javascript_method_invocation,
)
from model.core_model import (
    FindingEnum,
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
    _, method = split_on_last_dot(invocation_step.method)
    if method not in {"createCipheriv", "createDecipheriv"}:
        return
    dependencies = get_dependencies(step_index, syntax_steps)
    algorithm = dependencies[-1]
    if (
        # pylint: disable=used-before-assignment
        algorithm.type == "SyntaxStepLiteral"
        and (algorithm_value := algorithm.value)
        and javascript_cipher_vulnerable(algorithm_value)
    ):
        yield get_vulnerabilities_from_n_ids(
            cwe=("310", "327"),
            desc_key=("src.lib_path.f052.insecure_cipher.description"),
            desc_params=dict(lang="JavaScript"),
            finding=FINDING,
            graph_shard_nodes=[(shard, invocation_step.meta.n_id)],
        )
    elif algorithm.type == "SyntaxStepSymbolLookup":
        append_label_input(shard.graph, "1", FINDING)
        mark_methods_sink(
            FINDING,
            shard.graph,
            shard.syntax,
            {"createCipheriv", "createDecipheriv"},
        )
        yield shard_n_id_query(graph_db, FINDING, shard, "1")
    else:
        return


def _test_crypto_js(
    shard: GraphShard,
    invocation_step: SyntaxStepMethodInvocation,
) -> Iterator[Vulnerability]:
    _methods = [
        ("crypto-js", "DES", "encrypt"),
        ("crypto-js", "RC4", "encrypt"),
    ]
    methods = set(
        chain.from_iterable(build_attr_paths(*method) for method in _methods)
    )
    _, method = split_on_first_dot(invocation_step.method)
    if method not in methods:
        return
        yield  # pylint: disable=unreachable
    yield get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key=("src.lib_path.f052.insecure_cipher.description"),
        desc_params=dict(lang="JavaScript"),
        finding=FINDING,
        graph_shard_nodes=[(shard, invocation_step.meta.n_id)],
    )


def insecure_cipher(
    graph_db: GraphDB,
) -> Vulnerabilities:
    def find_vulns() -> Iterator[Vulnerability]:
        for (
            shard,
            syntax_steps,
            invocation_step,
            index,
        ) in yield_javascript_method_invocation(graph_db):
            yield from _test_native_cipher(
                graph_db,
                shard,
                syntax_steps,
                index,
                invocation_step,
            )
            yield from _test_crypto_js(shard, invocation_step)

    return tuple(chain.from_iterable(find_vulns()))


def insecure_key(graph_db: GraphDB) -> Vulnerabilities:
    def find_vulns() -> Iterator[Vulnerability]:
        for (
            shard,
            syntax_steps,
            invocation_step,
            step_index,
        ) in yield_javascript_method_invocation(graph_db):
            _, method = split_on_last_dot(invocation_step.method)
            if method not in {"createECDH"}:
                continue
            dependencies = get_dependencies(step_index, syntax_steps)
            curve = dependencies[-1]
            if (
                # pylint: disable=used-before-assignment
                curve.type == "SyntaxStepLiteral"
                and (algorithm_value := curve.value)
                and insecure_elliptic_curve(algorithm_value)
            ):
                yield get_vulnerabilities_from_n_ids(
                    cwe=("310", "327"),
                    desc_key="src.lib_path.f052.insecure_key.description",
                    desc_params=dict(lang="JavaScript"),
                    finding=FINDING,
                    graph_shard_nodes=[(shard, invocation_step.meta.n_id)],
                )

    return tuple(chain.from_iterable(find_vulns()))


FINDING: FindingEnum = FindingEnum.F052
