from contextlib import (
    suppress,
)
from lib_root.utilities.kotlin import (
    yield_method_invocation,
)
from lib_sast.types import (
    ShardDb,
)
from model.core_model import (
    MethodsEnum,
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
from utils.crypto import (
    insecure_elliptic_curve,
)
import utils.graph as g
from utils.languages.java import (
    is_cipher_vulnerable as java_cipher_vulnerable,
)
from utils.string import (
    complete_attrs_on_set,
)


def security_yield_insecure_key(
    shard: GraphShard, type_name: str, parameters: List[Any]
) -> GraphShardNodes:
    insecure_rsa_spec = complete_attrs_on_set(
        {"security.spec.RSAKeyGenParameterSpec"}
    )
    insecure_ec_spec = complete_attrs_on_set(
        {"security.spec.ECGenParameterSpec"}
    )
    if parameters and type_name in insecure_rsa_spec:
        param_id = parameters[0]
        if param_text := shard.graph.nodes[param_id].get("label_text"):
            with suppress(TypeError):
                key_length = int(param_text)
                if key_length < 2048:
                    yield shard, param_id
    if parameters and type_name in insecure_ec_spec:
        param_id = parameters[0]
        if (
            param_text := shard.graph.nodes[param_id].get("label_text")
        ) and insecure_elliptic_curve(param_text.replace('"', "")):
            yield shard, param_id


def yield_insecure_hash(
    shard: GraphShard,
    method_name: str,
    method_id: str,
    parameters: List[Any],
) -> GraphShardNodes:
    insecure_digests = {
        "org.apache.commons.codec.digest.DigestUtils.getMd2Digest",
        "org.apache.commons.codec.digest.DigestUtils.getMd5Digest",
        "org.apache.commons.codec.digest.DigestUtils.getShaDigest",
        "org.apache.commons.codec.digest.DigestUtils.getSha1Digest",
        "org.apache.commons.codec.digest.DigestUtils.md2",
        "org.apache.commons.codec.digest.DigestUtils.md2Hex",
        "org.apache.commons.codec.digest.DigestUtils.md5",
        "org.apache.commons.codec.digest.DigestUtils.md5Hex",
        "org.apache.commons.codec.digest.DigestUtils.sha",
        "org.apache.commons.codec.digest.DigestUtils.shaHex",
        "org.apache.commons.codec.digest.DigestUtils.sha1",
        "org.apache.commons.codec.digest.DigestUtils.sha1Hex",
        "com.google.common.hash.Hashing.adler32",
        "com.google.common.hash.Hashing.crc32",
        "com.google.common.hash.Hashing.crc32c",
        "com.google.common.hash.Hashing.goodFastHash",
        "com.google.common.hash.Hashing.hmacMd5",
        "com.google.common.hash.Hashing.hmacSha1",
        "com.google.common.hash.Hashing.md5",
        "com.google.common.hash.Hashing.sha1",
        "java.security.spec.MGF1ParameterSpec.SHA1",
    }
    if method_name in complete_attrs_on_set(insecure_digests):
        yield shard, method_id
    if method_name in complete_attrs_on_set(
        {
            "java.security.MessageDigest.getInstance",
        }
    ):
        for param_id in parameters:
            if (
                param_text := shard.graph.nodes[param_id].get("label_text")
            ) and param_text.lower().replace('"', "") in {
                "md2",
                "md4",
                "md5",
                "sha1",
                "sha-1",
            }:
                yield shard, param_id


def yield_insecure_ciphers(
    shard: GraphShard, method_name: str, parameters: List[Any]
) -> GraphShardNodes:
    ciphers: Set[str] = complete_attrs_on_set(
        {
            "javax.crypto.Cipher.getInstance",
            "javax.crypto.KeyGenerator.getInstance",
        }
    )
    ssl_ciphers_safe: Set[str] = {
        "tls",
        "tlsv1.2",
        "tlsv1.3",
        "dtls",
        "dtlsv1.2",
        "dtlsv1.3",
    }
    ssl_ciphers: Set[str] = complete_attrs_on_set(
        {"javax.net.ssl.SSLContext.getInstance"}
    )

    if method_name not in ciphers | ssl_ciphers:
        return

    for param_id in parameters:
        param_type = shard.graph.nodes[param_id]["label_type"]
        param_text = shard.graph.nodes[param_id].get("label_text")

        is_cipher_vulnerable: bool = (
            method_name in ciphers
            and param_text
            and java_cipher_vulnerable(param_text)
        )
        is_ssl_cipher_vulnerable: bool = (
            method_name in ssl_ciphers
            and param_type in {"line_string_literal", "string_literal"}
            and param_text
            and param_text.lower()[1:-1] not in ssl_ciphers_safe
        )

        if is_cipher_vulnerable or is_ssl_cipher_vulnerable:
            yield shard, param_id


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
        yield from security_yield_insecure_key(shard, method_name, parameters)


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
        yield from yield_insecure_hash(
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
        yield from yield_insecure_ciphers(shard, method_name, parameters)
        yield from _okhttp_yield_insecure_ciphers(
            shard, method_name, parameters
        )


def kotlin_insecure_hash(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params=dict(lang="Kotlin"),
        graph_shard_nodes=_yield_insecure_hash(graph_db),
        method=MethodsEnum.KT_INSECURE_HASH,
    )


def kotlin_insecure_cipher(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="Kotlin"),
        graph_shard_nodes=_yield_insecure_ciphers(graph_db),
        method=MethodsEnum.KT_INSECURE_CIPHER,
    )


def kotlin_insecure_key(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params=dict(lang="Kotlin"),
        graph_shard_nodes=_yield_insecure_key(graph_db),
        method=MethodsEnum.KT_INSECURE_KEY,
    )
