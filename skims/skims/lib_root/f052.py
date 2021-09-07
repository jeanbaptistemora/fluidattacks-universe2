from contextlib import (
    suppress,
)
import itertools
from lib_root import (
    yield_go_member_access,
    yield_go_object_creation,
    yield_java_method_invocation,
    yield_java_object_creation,
    yield_kotlin_method_invocation,
)
from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from sast_syntax_readers.kotlin.common import (
    get_composite_name,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
)
from utils import (
    graph as g,
)
from utils.graph.transformation import (
    build_member_access_expression_key,
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


def _csharp_yield_member_access(
    graph_db: graph_model.GraphDB, members: Set[str]
) -> graph_model.GraphShardNodes:
    for shard in graph_db.shards_by_language(
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
    for shard, method_id, method_name in yield_java_method_invocation(
        graph_db
    ):
        match = g.match_ast_group(
            shard.graph,
            method_id,
            "argument_list",
        )
        parameters = g.adj_ast(
            shard.graph,
            match["argument_list"][0],
        )[1:-1]
        yield from _javax_yield_insecure_ciphers(
            shard, method_name, parameters
        )


def _javax_yield_insecure_ciphers(
    shard: graph_model.GraphShard, method_name: str, parameters: List[Any]
) -> graph_model.GraphShardNodes:
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
            and _vuln_cipher_get_instance(param_text)
        )
        is_ssl_cipher_vulnerable: bool = (
            method_name in ssl_ciphers
            and param_type in {"line_string_literal", "string_literal"}
            and param_text
            and param_text.lower()[1:-1] not in ssl_ciphers_safe
        )

        if is_cipher_vulnerable or is_ssl_cipher_vulnerable:
            yield shard, param_id


def _java_yield_insecure_hash(
    graph_db: graph_model.GraphDB,
) -> graph_model.GraphShardNodes:
    for shard, method_id, method_name in yield_java_method_invocation(
        graph_db
    ):
        match = g.match_ast_group(
            shard.graph,
            method_id,
            "argument_list",
        )
        parameters = g.adj_ast(
            shard.graph,
            match["argument_list"][0],
        )[1:-1]
        yield from _jvm_yield_insecure_hash(
            shard, method_name, method_id, parameters
        )


def _java_yield_insecure_key(
    graph_db: graph_model.GraphDB,
) -> graph_model.GraphShardNodes:
    for shard, object_id, type_name in yield_java_object_creation(graph_db):
        match = g.match_ast(
            shard.graph,
            object_id,
            "argument_list",
        )
        parameters = g.adj_ast(
            shard.graph,
            match["argument_list"],
        )[1:-1]
        yield from _java_security_yield_insecure_key(
            shard,
            type_name,
            parameters,
        )


def _java_security_yield_insecure_key(
    shard: graph_model.GraphShard, type_name: str, parameters: List[Any]
) -> graph_model.GraphShardNodes:
    insecure_stds = {
        "secp112r1",
        "secp112r2",
        "secp128r1",
        "secp128r2",
        "secp160k1",
        "secp160r1",
        "secp160r2",
        "secp192k1",
        "prime192v1",
        "prime192v2",
        "prime192v3",
        "sect113r1",
        "sect113r2",
        "sect131r1",
        "sect131r2",
        "sect163k1",
        "sect163r1",
        "sect163r2",
        "sect193r1",
        "sect193r2",
        "c2pnb163v1",
        "c2pnb163v2",
        "c2pnb163v3",
        "c2pnb176v1",
        "c2tnb191v1",
        "c2tnb191v2",
        "c2tnb191v3",
        "c2pnb208w1",
        "wap-wsg-idm-ecid-wtls1",
        "wap-wsg-idm-ecid-wtls3",
        "wap-wsg-idm-ecid-wtls4",
        "wap-wsg-idm-ecid-wtls5",
        "wap-wsg-idm-ecid-wtls6",
        "wap-wsg-idm-ecid-wtls7",
        "wap-wsg-idm-ecid-wtls8",
        "wap-wsg-idm-ecid-wtls9",
        "wap-wsg-idm-ecid-wtls10",
        "wap-wsg-idm-ecid-wtls11",
        "oakley-ec2n-3",
        "oakley-ec2n-4",
        "brainpoolp160r1",
        "brainpoolp160t1",
        "brainpoolp192r1",
        "brainpoolp192t1",
    }
    insecure_rsa_spec = complete_attrs_on_set(
        {"java.security.spec.RSAKeyGenParameterSpec"}
    )
    insecure_ec_spec = complete_attrs_on_set(
        {"java.security.spec.ECGenParameterSpec"}
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
        ) and param_text.replace('"', "") in insecure_stds:
            yield shard, param_id


def _java_yield_insecure_pass(
    graph_db: graph_model.GraphDB,
) -> graph_model.GraphShardNodes:
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
    for shard, object_id, type_name in yield_java_object_creation(graph_db):
        if type_name in insecure_instances:
            yield shard, object_id


def _jvm_yield_insecure_hash(
    shard: graph_model.GraphShard,
    method_name: str,
    method_id: str,
    parameters: List[Any],
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


def _csharp_yield_object_creation(
    graph_db: graph_model.GraphDB, members: Set[str]
) -> graph_model.GraphShardNodes:
    for shard in graph_db.shards_by_language(
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


def _kotlin_yield_insecure_ciphers(
    graph_db: graph_model.GraphDB,
) -> graph_model.GraphShardNodes:
    for shard, method_id, method_name in yield_kotlin_method_invocation(
        graph_db
    ):
        match = g.match_ast_group(
            shard.graph, method_id, "value_argument", depth=3
        )
        parameters = [
            g.adj_ast(shard.graph, argument_id)[0]
            for argument_id in match["value_argument"]
        ]
        yield from _javax_yield_insecure_ciphers(
            shard, method_name, parameters
        )
        yield from _okhttp_yield_insecure_ciphers(
            shard, method_name, parameters
        )


def _kotlin_yield_insecure_hash(
    graph_db: graph_model.GraphDB,
) -> graph_model.GraphShardNodes:
    for shard, method_id, method_name in yield_kotlin_method_invocation(
        graph_db
    ):
        match = g.match_ast_group(
            shard.graph, method_id, "value_argument", depth=3
        )
        parameters = [
            g.adj_ast(shard.graph, argument_id)[0]
            for argument_id in match["value_argument"]
        ]
        yield from _jvm_yield_insecure_hash(
            shard, method_name, method_id, parameters
        )


def _kotlin_yield_insecure_key(
    graph_db: graph_model.GraphDB,
) -> graph_model.GraphShardNodes:
    for shard, method_id, method_name in yield_kotlin_method_invocation(
        graph_db
    ):
        match = g.match_ast_group(
            shard.graph, method_id, "value_argument", depth=3
        )
        parameters = [
            g.adj_ast(shard.graph, argument_id)[0]
            for argument_id in match["value_argument"]
        ]
        yield from _java_security_yield_insecure_key(
            shard, method_name, parameters
        )


def _okhttp_yield_insecure_ciphers(
    shard: graph_model.GraphShard, method_name: str, parameters: List[Any]
) -> graph_model.GraphShardNodes:
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


def csharp_insecure_hash(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    insecure_ciphers = {
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
        yield from _csharp_yield_member_access(graph_db, insecure_ciphers)
        yield from _csharp_yield_object_creation(graph_db, insecure_ciphers)

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
    insecure_ciphers = {
        "AesFastEngine",
        "DES",
        "DESCryptoServiceProvider",
        "TripleDES",
        "TripleDESCng",
        "DesEdeEngine",
        "TripleDESCryptoServiceProvider",
        "RC2",
        "RC2CryptoServiceProvider",
        "DSACryptoServiceProvider",
    }

    def n_ids() -> graph_model.GraphShardNodes:
        yield from _csharp_yield_member_access(graph_db, insecure_ciphers)
        yield from _csharp_yield_object_creation(graph_db, insecure_ciphers)

    return get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="CSharp"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def csharp_aesmanaged_secure_mode(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    unsafe_modes = {
        "CipherMode.ECB",
        "CipherMode.OFB",
        "CipherMode.CFB",
    }

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            for member in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(
                    label_type="object_creation_expression"
                ),
            ):
                match_object_creation = g.match_ast(
                    shard.graph, member, "__0__"
                )

                if (
                    shard.graph.nodes[match_object_creation["__1__"]].get(
                        "label_text"
                    )
                    == "AesManaged"
                ) and check_props(shard.graph, match_object_creation):
                    yield shard, member

    def check_props(
        graph: graph_model.GraphShard, match: Dict[str, Optional[str]]
    ) -> bool:
        insecure = False
        props = g.get_ast_childs(
            graph, match["__2__"], "member_access_expression", depth=2
        )

        for prop in props:
            mode = build_member_access_expression_key(
                graph,
                prop,
            )
            if mode in unsafe_modes:
                insecure = True

        return insecure

    return get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="CSharp"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def csharp_rsa_secure_mode(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    name_vars = []

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            for member in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(
                    label_type="object_creation_expression"
                ),
            ):
                object_creation = g.match_ast(shard.graph, member, "__0__")
                if (
                    shard.graph.nodes[object_creation["__1__"]].get(
                        "label_text"
                    )
                    == "RSACryptoServiceProvider"
                ):
                    node_var = g.get_ast_childs(
                        shard.graph,
                        g.pred_ast(shard.graph, member, depth=2)[1],
                        "identifier",
                    )[0]
                    name_vars.append(
                        shard.graph.nodes[node_var].get("label_text")
                    )
            for member in g.filter_nodes(
                shard.graph,
                nodes=shard.graph.nodes,
                predicate=g.pred_has_labels(
                    label_type="member_access_expression",
                ),
            ):
                prop = build_member_access_expression_key(
                    shard.graph,
                    member,
                )
                method = prop.split(".")
                if method[0] in name_vars and method[1] == "Encrypt":
                    member_encrypt = g.pred(shard.graph, member)[0]
                    arg_bool = g.get_ast_childs(
                        shard.graph, member_encrypt, "boolean_literal", depth=3
                    )
                    if (
                        len(arg_bool) > 0
                        and shard.graph.nodes[arg_bool[0]].get("label_text")
                        == "false"
                    ):
                        yield shard, member

    return get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="CSharp"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def csharp_insecure_keys(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:

    ciphers = {
        "RSACryptoServiceProvider",
        "DSACng",
        "RSACng",
    }

    def n_ids() -> graph_model.GraphShardNodes:
        for shard, member in itertools.chain(
            _csharp_yield_object_creation(graph_db, ciphers),
        ):
            args_list = g.get_ast_childs(shard.graph, member, "argument_list")
            keys = g.get_ast_childs(
                shard.graph, args_list[0], "integer_literal", depth=2
            )
            if keys:
                for key in keys:
                    if int(shard.graph.nodes[key].get("label_text")) < 2048:
                        yield shard, member
            else:
                object_name = g.match_ast(shard.graph, member)["__1__"]
                if (
                    shard.graph.nodes[object_name].get("label_text")
                    == "RSACryptoServiceProvider"
                ):
                    yield shard, member

    return get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="CSharp"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def go_insecure_cipher(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    insecure_ciphers = {
        "des",
        "NewTripleDESCipher",
    }

    def n_ids() -> graph_model.GraphShardNodes:
        yield from yield_go_member_access(graph_db, insecure_ciphers)
        yield from yield_go_object_creation(graph_db, insecure_ciphers)

    return get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="Go"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def go_insecure_hash(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:

    insecure_ciphers = {"md4", "md5", "ripemd160", "sha1"}

    def n_ids() -> graph_model.GraphShardNodes:
        yield from yield_go_object_creation(graph_db, insecure_ciphers)

    return get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params=dict(lang="Go"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def java_insecure_cipher(
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


def java_insecure_key(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params=dict(lang="Java"),
        finding=FINDING,
        graph_shard_nodes=_java_yield_insecure_key(graph_db),
    )


def java_insecure_pass(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key="src.lib_path.f052.insecure_pass.description",
        desc_params=dict(lang="Java"),
        finding=FINDING,
        graph_shard_nodes=_java_yield_insecure_pass(graph_db),
    )


def kotlin_insecure_cipher(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="Kotlin"),
        finding=FINDING,
        graph_shard_nodes=_kotlin_yield_insecure_ciphers(graph_db),
    )


def kotlin_insecure_hash(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params=dict(lang="Kotlin"),
        finding=FINDING,
        graph_shard_nodes=_kotlin_yield_insecure_hash(graph_db),
    )


def kotlin_insecure_key(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    return get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params=dict(lang="Kotlin"),
        finding=FINDING,
        graph_shard_nodes=_kotlin_yield_insecure_key(graph_db),
    )


# Constants
FINDING: core_model.FindingEnum = core_model.FindingEnum.F052
QUERIES: graph_model.Queries = (
    (FINDING, csharp_insecure_hash),
    (FINDING, csharp_insecure_cipher),
    (FINDING, csharp_aesmanaged_secure_mode),
    (FINDING, csharp_rsa_secure_mode),
    (FINDING, go_insecure_cipher),
    (FINDING, go_insecure_hash),
    (FINDING, java_insecure_cipher),
    (FINDING, java_insecure_hash),
    (FINDING, java_insecure_key),
    (FINDING, java_insecure_pass),
    (FINDING, kotlin_insecure_cipher),
    (FINDING, kotlin_insecure_hash),
    (FINDING, kotlin_insecure_key),
)
