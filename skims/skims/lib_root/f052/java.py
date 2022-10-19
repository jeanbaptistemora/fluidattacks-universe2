# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from contextlib import (
    suppress,
)
from lib_root.utilities.common import (
    search_method_invocation_naive,
)
from lib_root.utilities.java import (
    yield_method_invocation_syntax_graph,
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


def is_insecure_key_argument(triggers: Set[str], check: str) -> bool:
    eval_str = "".join(list(triggers))
    if check == "RSA":
        with suppress(TypeError):
            key_length = int(eval_str)
            if key_length < 2048:
                return True
    if check == "EC":
        return insecure_elliptic_curve(eval_str)
    return False


def eval_insecure_key(graph: Graph, n_id: NId) -> bool:
    method = MethodsEnum.JAVA_INSECURE_KEY
    insecure_rsa_spec = complete_attrs_on_set(
        {"java.security.spec.RSAKeyGenParameterSpec"}
    )
    insecure_ec_spec = complete_attrs_on_set(
        {"java.security.spec.ECGenParameterSpec"}
    )

    oc_attrs = graph.nodes[n_id]
    check = None
    if oc_attrs["name"] in insecure_ec_spec:
        check = "EC"
    if oc_attrs["name"] in insecure_rsa_spec:
        check = "RSA"

    if (
        check
        and (al_id := oc_attrs.get("arguments_id"))
        and (param := g.match_ast(graph, al_id).get("__0__"))
    ):
        for path in get_backward_paths(graph, param):
            evaluation = evaluate(method, graph, path, param)
            if evaluation and is_insecure_key_argument(
                evaluation.triggers, check
            ):
                return True
    return False


def is_insecure_hash_argument(graph: Graph, param: NId) -> bool:
    method = MethodsEnum.JAVA_INSECURE_HASH
    for path in get_backward_paths(graph, param):
        evaluation = evaluate(method, graph, path, param)
        if evaluation and evaluation.danger:
            return True
    return False


def eval_insecure_hash(graph: Graph, m_id: NId, m_name: str) -> bool:
    insecure_digests_1 = complete_attrs_on_set(
        {
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
    )
    insecure_digests_2 = complete_attrs_on_set(
        {"java.security.MessageDigest.getInstance"}
    )

    if m_name in insecure_digests_1:
        return True

    if m_name in insecure_digests_2:
        mi_attrs = graph.nodes[m_id]
        m_al = g.adj_ast(graph, mi_attrs.get("arguments_id"))
        is_insecure = []
        for argument in m_al:
            res = is_insecure_hash_argument(graph, argument)
            is_insecure.append(res)
        if any(is_insecure):
            return True

    return False


def is_insecure_cipher_argument(graph: Graph, param: NId, check: str) -> bool:
    method = MethodsEnum.JAVA_INSECURE_CIPHER
    ssl_safe_methods = {
        "tlsv1.2",
        "tlsv1.3",
        "dtlsv1.2",
        "dtlsv1.3",
    }
    for path in get_backward_paths(graph, param):
        if (
            evaluation := evaluate(method, graph, path, param)
        ) and evaluation.triggers != set():
            cipher = "".join(list(evaluation.triggers)).lower()
            if (check == "CR" and java_cipher_vulnerable(cipher)) or (
                check == "SSL" and cipher not in ssl_safe_methods
            ):
                return True
    return False


def eval_insecure_cipher(graph: Graph, m_id: NId, m_name: str) -> bool:
    ciphers = complete_attrs_on_set(
        {
            "javax.crypto.Cipher.getInstance",
            "javax.crypto.KeyGenerator.getInstance",
        }
    )
    ssl_ciphers = complete_attrs_on_set(
        {"javax.net.ssl.SSLContext.getInstance"}
    )

    if m_name in ciphers:
        check = "CR"
    elif m_name in ssl_ciphers:
        check = "SSL"
    else:
        return False

    mi_attrs = graph.nodes[m_id]
    m_al = g.adj_ast(graph, mi_attrs.get("arguments_id"))
    is_insecure = []
    for argument in m_al:
        res = is_insecure_cipher_argument(graph, argument, check)
        is_insecure.append(res)

    if any(is_insecure):
        return True
    return False


def is_insecure_connection(graph: Graph, n_id: NId) -> bool:
    method = MethodsEnum.JAVA_INSECURE_CONNECTION
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def java_insecure_pass(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
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

    def n_ids() -> Iterable[GraphShardNode]:
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
        method=MethodsEnum.JAVA_INSECURE_PASS,
    )


def java_insecure_key(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    def n_ids() -> Iterable[GraphShardNode]:
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
                if eval_insecure_key(graph, n_id):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_INSECURE_KEY,
    )


def java_insecure_hash(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for m_id, m_name in yield_method_invocation_syntax_graph(graph):
                if eval_insecure_hash(graph, m_id, m_name):
                    yield shard, m_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_INSECURE_HASH,
    )


def java_insecure_cipher(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for m_id, m_name in yield_method_invocation_syntax_graph(graph):
                if eval_insecure_cipher(graph, m_id, m_name):
                    yield shard, m_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_INSECURE_CIPHER,
    )


def java_insecure_connection(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in search_method_invocation_naive(graph, {"tlsVersions"}):
                if (args_id := graph.nodes[nid].get("arguments_id")) and (
                    is_insecure_connection(graph, args_id)
                ):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_connection.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_INSECURE_CONNECTION,
    )
