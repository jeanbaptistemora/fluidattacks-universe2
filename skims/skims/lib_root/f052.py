from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from typing import (
    Iterable,
    Set,
    Tuple,
)
from utils import (
    graph as g,
)
from utils.string import (
    complete_attrs_on_set,
)


def _vuln_cipher_get_instance(transformation: str) -> bool:
    alg, mode, pad, *_ = (
        transformation.lower().replace('"', "") + "///"
    ).split("/", 3)

    return any(
        (
            alg == "aes" and mode == "ecb",
            alg == "aes" and mode == "cbc" and pad and pad != "nopadding",
            alg == "blowfish",
            alg == "des",
            alg == "desede",
            alg == "rc2",
            alg == "rc4",
            alg == "rsa" and "oaep" not in pad,
        )
    )


def _yield_java_method_invocation(
    graph_db: graph_model.GraphDB,
) -> Iterable[Tuple[graph_model.GraphShard, str, str]]:
    for shard in graph_db.shards_by_langauge(
        graph_model.GraphShardMetadataLanguage.JAVA,
    ):
        for method_id in g.filter_nodes(
            shard.graph,
            nodes=shard.graph.nodes,
            predicate=g.pred_has_labels(label_type="method_invocation"),
        ):
            match = g.match_ast_group(
                shard.graph,
                method_id,
                "argument_list",
                "identifier",
                "field_access",
            )
            method_name = g.concatenate_label_text(
                shard.graph, match["identifier"], separator="."
            )
            if match["field_access"]:
                base_name = shard.graph.nodes[match["field_access"][0]][
                    "label_text"
                ]
                method_name = base_name + "." + method_name
            yield shard, method_id, method_name


def _csharp_yield_member_access(
    graph_db: graph_model.GraphDB, members: Set[str]
) -> graph_model.GraphShardNodes:
    for shard in graph_db.shards_by_langauge(
        graph_model.GraphShardMetadataLanguage.CSHARP,
    ):
        for member in g.filter_nodes(
            shard.graph,
            nodes=shard.graph.nodes,
            predicate=g.pred_has_labels(label_type="member_access_expression"),
        ):
            match = g.match_ast(shard.graph, member, "__0__")
            if shard.graph.nodes[match["__0__"]].get("label_text") in members:
                yield shard, member


def _java_yield_insecure_ciphers(
    graph_db: graph_model.GraphDB,
) -> graph_model.GraphShardNodes:
    for shard, method_id, method_name in _yield_java_method_invocation(
        graph_db
    ):
        match = g.match_ast_group(
            shard.graph,
            method_id,
            "argument_list",
        )
        if method_name not in complete_attrs_on_set(
            {
                "javax.crypto.Cipher.getInstance",
                "javax.crypto.KeyGenerator.getInstance",
                "javax.net.ssl.SSLContext.getInstance",
            }
        ):
            continue
        parameters = g.adj_ast(
            shard.graph,
            match["argument_list"][0],
        )[1:-1]
        for param_id in parameters:
            if param_text := shard.graph.nodes[param_id].get("label_text"):
                if (
                    method_name
                    in complete_attrs_on_set(
                        {
                            "javax.crypto.Cipher.getInstance",
                            "javax.crypto.KeyGenerator.getInstance",
                        }
                    )
                    and _vuln_cipher_get_instance(param_text)
                ):
                    yield shard, param_id
                elif method_name in complete_attrs_on_set(
                    {
                        "javax.net.ssl.SSLContext.getInstance",
                    }
                ) and param_id not in {
                    "tls",
                    "tlsv1.2",
                    "tlsv1.3",
                    "dtls",
                    "dtlsv1.2",
                    "dtlsv1.3",
                }:
                    yield shard, param_id


def _java_yield_insecure_hash(
    graph_db: graph_model.GraphDB,
) -> graph_model.GraphShardNodes:
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
    }
    for shard, method_id, method_name in _yield_java_method_invocation(
        graph_db
    ):
        if method_name in complete_attrs_on_set(insecure_digests):
            yield shard, method_id
            continue

        match = g.match_ast_group(
            shard.graph,
            method_id,
            "argument_list",
        )
        if method_name not in complete_attrs_on_set(
            {
                "java.security.MessageDigest.getInstance",
            }
        ):
            continue
        parameters = g.adj_ast(
            shard.graph,
            match["argument_list"][0],
        )[1:-1]
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


def _csharp_yield_object_creation(
    graph_db: graph_model.GraphDB, members: Set[str]
) -> graph_model.GraphShardNodes:
    for shard in graph_db.shards_by_langauge(
        graph_model.GraphShardMetadataLanguage.CSHARP,
    ):
        for member in g.filter_nodes(
            shard.graph,
            nodes=shard.graph.nodes,
            predicate=g.pred_has_labels(
                label_type="object_creation_expression"
            ),
        ):
            match = g.match_ast(shard.graph, member, "identifier")
            if (identifier := match["identifier"]) and shard.graph.nodes[
                identifier
            ]["label_text"] in members:
                yield shard, member


def csharp_insecure_hash(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    insecure_cyphers = {
        "HMACMD5",
        "HMACRIPEMD160",
        "HMACSHA1",
        "MACTripleDES",
        "MD5",
        "MD5Cng",
        "MD5CryptoServiceProvider",
        "MD5Managed",
        "RIPEMD160",
        "RIPEMD160Managed",
        "SHA1",
        "SHA1Cng",
        "SHA1CryptoServiceProvider",
        "SHA1Managed",
    }

    def n_ids() -> graph_model.GraphShardNodes:
        yield from _csharp_yield_member_access(graph_db, insecure_cyphers)
        yield from _csharp_yield_object_creation(graph_db, insecure_cyphers)

    return get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params=dict(lang="CSharp"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def csharp_insecure_cipher(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    insecure_cyphers = {
        "DES",
        "DESCryptoServiceProvider",
        "TripleDES",
        "TripleDESCng",
        "TripleDESCryptoServiceProvider",
        "RC2",
        "RC2CryptoServiceProvider",
    }

    def n_ids() -> graph_model.GraphShardNodes:
        yield from _csharp_yield_member_access(graph_db, insecure_cyphers)
        yield from _csharp_yield_object_creation(graph_db, insecure_cyphers)

    return get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="CSharp"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def java_insecure_cypher(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="Java"),
        finding=FINDING,
        graph_shard_nodes=_java_yield_insecure_ciphers(graph_db),
    )


def java_insecure_hash(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params=dict(lang="Java"),
        finding=FINDING,
        graph_shard_nodes=_java_yield_insecure_hash(graph_db),
    )


# Constants
FINDING: core_model.FindingEnum = core_model.FindingEnum.F052
QUERIES: graph_model.Queries = (
    (FINDING, csharp_insecure_hash),
    (FINDING, csharp_insecure_cipher),
    (FINDING, java_insecure_cypher),
    (FINDING, java_insecure_hash),
)
