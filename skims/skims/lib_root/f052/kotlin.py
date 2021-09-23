from lib_root.f052.java import (
    javax_yield_insecure_ciphers,
    jvm_yield_insecure_hash,
    security_yield_insecure_key as java_security_yield_insecure_key,
)
from lib_root.utilities.kotlin import (
    yield_method_invocation,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphDB,
    GraphShard,
    GraphShardNodes,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from sast_syntax_readers.kotlin.common import (
    get_composite_name,
)
from typing import (
    Any,
    List,
    Set,
)
import utils.graph as g
from utils.string import (
    complete_attrs_on_set,
)


def _yield_insecure_key(
    graph_db: GraphDB,
) -> GraphShardNodes:
    for shard, method_id, method_name in yield_method_invocation(graph_db):
        match = g.match_ast_group(
            shard.graph, method_id, "value_argument", depth=3
        )
        parameters = [
            g.adj_ast(shard.graph, argument_id)[0]
            for argument_id in match["value_argument"]
        ]
        yield from java_security_yield_insecure_key(
            shard, method_name, parameters
        )


def _yield_insecure_hash(
    graph_db: GraphDB,
) -> GraphShardNodes:
    for shard, method_id, method_name in yield_method_invocation(graph_db):
        match = g.match_ast_group(
            shard.graph, method_id, "value_argument", depth=3
        )
        parameters = [
            g.adj_ast(shard.graph, argument_id)[0]
            for argument_id in match["value_argument"]
        ]
        yield from jvm_yield_insecure_hash(
            shard, method_name, method_id, parameters
        )


def _okhttp_yield_insecure_ciphers(
    shard: GraphShard, method_name: str, parameters: List[Any]
) -> GraphShardNodes:
    ssl_cipher_method: Set[str] = complete_attrs_on_set(
        {"ConnectionSpec.Builder.tlsVersions"}
    )
    insecure_ciphers: Set[str] = {
        "SSL_3_0",
        "TLS_1_0",
        "TLS_1_1",
    }
    if parameters and method_name in ssl_cipher_method:
        param_id = parameters[0]
        param_value = get_composite_name(
            shard.graph, g.pred_ast(shard.graph, param_id)[0]
        )
        ssl_version = param_value.split(".")[-1]
        if ssl_version in insecure_ciphers:
            yield shard, param_id


def _yield_insecure_ciphers(
    graph_db: GraphDB,
) -> GraphShardNodes:
    for shard, method_id, method_name in yield_method_invocation(graph_db):
        match = g.match_ast_group(
            shard.graph, method_id, "value_argument", depth=3
        )
        parameters = [
            g.adj_ast(shard.graph, argument_id)[0]
            for argument_id in match["value_argument"]
        ]
        yield from javax_yield_insecure_ciphers(shard, method_name, parameters)
        yield from _okhttp_yield_insecure_ciphers(
            shard, method_name, parameters
        )


def insecure_hash(
    graph_db: GraphDB,
) -> Vulnerabilities:
    return get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params=dict(lang="Kotlin"),
        finding=FINDING,
        graph_shard_nodes=_yield_insecure_hash(graph_db),
    )


def insecure_cipher(
    graph_db: GraphDB,
) -> Vulnerabilities:
    return get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="Kotlin"),
        finding=FINDING,
        graph_shard_nodes=_yield_insecure_ciphers(graph_db),
    )


def insecure_key(
    graph_db: GraphDB,
) -> Vulnerabilities:
    return get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params=dict(lang="Kotlin"),
        finding=FINDING,
        graph_shard_nodes=_yield_insecure_key(graph_db),
    )


FINDING: FindingEnum = FindingEnum.F052
