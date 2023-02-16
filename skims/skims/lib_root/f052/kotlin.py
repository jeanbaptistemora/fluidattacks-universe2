from collections.abc import (
    Iterator,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    Graph,
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
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
import utils.graph as g
from utils.string import (
    complete_attrs_on_set,
)


def get_eval_result(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def kotlin_insecure_hash(
    graph_db: GraphDB,
) -> Vulnerabilities:
    danger_methods = complete_attrs_on_set(
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

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.KOTLIN):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(
                graph,
                label_type="MethodInvocation",
            ):
                n_attrs = graph.nodes[n_id]
                if n_attrs["expression"] in danger_methods:
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.KT_INSECURE_HASH,
    )


def kotlin_insecure_hash_instance(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.KT_INSECURE_HASH
    danger_methods = complete_attrs_on_set(
        {
            "java.security.MessageDigest.getInstance",
        }
    )

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.KOTLIN):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(
                graph,
                label_type="MethodInvocation",
            ):
                n_attrs = graph.nodes[n_id]
                if (
                    n_attrs["expression"] in danger_methods
                    and (al_id := graph.nodes[n_id].get("arguments_id"))
                    and (arg_id := g.match_ast(graph, al_id).get("__0__"))
                    and get_eval_result(graph, arg_id, method)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def kotlin_insecure_cipher(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.KT_INSECURE_CIPHER
    danger_methods = complete_attrs_on_set(
        {
            "javax.crypto.Cipher.getInstance",
            "javax.crypto.KeyGenerator.getInstance",
        }
    )

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.KOTLIN):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(
                graph,
                label_type="MethodInvocation",
            ):
                n_attrs = graph.nodes[n_id]
                if (
                    n_attrs["expression"] in danger_methods
                    and (al_id := graph.nodes[n_id].get("arguments_id"))
                    and (arg_id := g.match_ast(graph, al_id).get("__0__"))
                    and get_eval_result(graph, arg_id, method)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def kotlin_insecure_cipher_ssl(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.KT_INSECURE_CIPHER_SSL
    danger_methods = complete_attrs_on_set(
        {"javax.net.ssl.SSLContext.getInstance"}
    )

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.KOTLIN):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(
                graph,
                label_type="MethodInvocation",
            ):
                n_attrs = graph.nodes[n_id]
                if (
                    n_attrs["expression"] in danger_methods
                    and (al_id := graph.nodes[n_id].get("arguments_id"))
                    and (arg_id := g.match_ast(graph, al_id).get("__0__"))
                    and get_eval_result(graph, arg_id, method)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def kotlin_insecure_cipher_http(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.KT_INSECURE_CIPHER_HTTP
    danger_methods = {"tlsVersions"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.KOTLIN):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(
                graph,
                label_type="MethodInvocation",
            ):
                m_names = graph.nodes[n_id]["expression"].split(".")
                if (
                    m_names[-1] in danger_methods
                    and (al_id := graph.nodes[n_id].get("arguments_id"))
                    and (arg_id := g.match_ast(graph, al_id).get("__0__"))
                    and get_eval_result(graph, arg_id, method)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def kotlin_insecure_key_rsa(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.KT_INSECURE_KEY
    danger_methods = complete_attrs_on_set(
        {"security.spec.RSAKeyGenParameterSpec"}
    )

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.KOTLIN):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(
                graph,
                label_type="MethodInvocation",
            ):
                n_attrs = graph.nodes[n_id]
                if (
                    n_attrs["expression"] in danger_methods
                    and (al_id := graph.nodes[n_id].get("arguments_id"))
                    and (arg_id := g.match_ast(graph, al_id).get("__0__"))
                    and get_eval_result(graph, arg_id, method)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def kotlin_insecure_key_ec(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.KT_INSECURE_KEY_EC
    danger_methods = complete_attrs_on_set(
        {"security.spec.ECGenParameterSpec"}
    )

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.KOTLIN):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(
                graph,
                label_type="MethodInvocation",
            ):
                n_attrs = graph.nodes[n_id]
                if (
                    n_attrs["expression"] in danger_methods
                    and (al_id := graph.nodes[n_id].get("arguments_id"))
                    and (arg_id := g.match_ast(graph, al_id).get("__0__"))
                    and get_eval_result(graph, arg_id, method)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
