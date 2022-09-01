from contextlib import (
    suppress,
)
from lib_root.utilities.java import (
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
    GraphShardMetadataLanguage,
    GraphShardNodes,
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


def is_insecure_argument(triggers: Set[str], check: str = "RSA") -> bool:
    eval_str = "".join(list(triggers))
    print(eval_str)
    if check == "RSA":
        with suppress(TypeError):
            key_length = int(eval_str)
            if key_length < 2048:
                return True
    if check == "EC":
        return insecure_elliptic_curve(eval_str)
    return False


def jvm_yield_insecure_hash(
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


def _yield_insecure_hash(
    graph_db: GraphDB,
) -> GraphShardNodes:
    for shard, method_id, method_name in yield_method_invocation(graph_db):
        match = g.match_ast_group(
            shard.graph,
            method_id,
            "argument_list",
        )
        parameters = g.adj_ast(
            shard.graph,
            match["argument_list"][0],
        )[1:-1]
        yield from jvm_yield_insecure_hash(
            shard, method_name, method_id, list(parameters)
        )


def javax_yield_insecure_ciphers(
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


def _yield_insecure_ciphers(
    graph_db: GraphDB,
) -> GraphShardNodes:
    for shard, method_id, method_name in yield_method_invocation(graph_db):
        match = g.match_ast_group(
            shard.graph,
            method_id,
            "argument_list",
        )
        parameters = g.adj_ast(
            shard.graph,
            match["argument_list"][0],
        )[1:-1]
        yield from javax_yield_insecure_ciphers(
            shard, method_name, list(parameters)
        )


def java_insecure_pass(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_INSECURE_PASS
    framework = "org.springframework.security"
    insecure_instances = complete_attrs_on_set(
        {
            f"{framework}.authentication.encoding.ShaPasswordEncoder",
            f"{framework}.authentication.encoding.Md5PasswordEncoder",
            f"{framework}.crypto.password.LdapShaPasswordEncoder",
            f"{framework}.crypto.password.Md4PasswordEncoder",
            f"{framework}.crypto.password.MessageDigestPasswordEncoder",
            f"{framework}.crypto.password.NoOpPasswordEncoder",
            f"{framework}.crypto.password.StandardPasswordEncoder",
            f"{framework}.crypto.scrypt.SCryptPasswordEncoder",
        }
    )

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="ObjectCreation"),
            ):
                if graph.nodes[n_id]["name"] in insecure_instances:
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_pass.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def java_insecure_key(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_INSECURE_KEY
    insecure_rsa_spec = complete_attrs_on_set(
        {"java.security.spec.RSAKeyGenParameterSpec"}
    )
    insecure_ec_spec = complete_attrs_on_set(
        {"java.security.spec.ECGenParameterSpec"}
    )

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="ObjectCreation"),
            ):
                oc_attrs = graph.nodes[n_id]
                check = None
                if oc_attrs["name"] in insecure_ec_spec:
                    check = "EC"
                if oc_attrs["name"] in insecure_rsa_spec:
                    check = "RSA"

                if check and (
                    param := g.match_ast(
                        graph, oc_attrs.get("arguments_id")
                    ).get("__0__")
                ):
                    for path in get_backward_paths(graph, param):
                        evaluation = evaluate(method, graph, path, param)
                        if evaluation and is_insecure_argument(
                            evaluation.triggers, check
                        ):
                            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def java_insecure_hash(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params=dict(lang="Java"),
        graph_shard_nodes=_yield_insecure_hash(graph_db),
        method=MethodsEnum.JAVA_INSECURE_HASH,
    )


def java_insecure_cipher(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="Java"),
        graph_shard_nodes=_yield_insecure_ciphers(graph_db),
        method=MethodsEnum.JAVA_INSECURE_CIPHER,
    )
