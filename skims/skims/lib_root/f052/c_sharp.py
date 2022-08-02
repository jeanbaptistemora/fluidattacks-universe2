from itertools import (
    chain,
)
from lib_root.utilities.c_sharp import (
    check_member_acces_expression,
    yield_shard_member_access,
    yield_shard_object_creation,
    yield_syntax_graph_member_access,
    yield_syntax_graph_object_creation,
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
    GraphShard,
    GraphShardMetadataLanguage,
    GraphShardNodes,
    MetadataGraphShardNodes,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
    get_vulnerabilities_from_n_ids_metadata,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    filter_ast,
    get_backward_paths,
)
from typing import (
    Dict,
    Optional,
    Set,
)
import utils.graph as g
from utils.graph.text_nodes import (
    node_to_str,
)
from utils.string import (
    build_attr_paths,
)


def _new_insecure_keys_check(
    shard: GraphShard, ciphers: Set[str]
) -> GraphShardNodes:
    graph = shard.syntax_graph
    for n_id in (
        filter_ast(graph, "1", types={"ObjectCreation"}) if graph else []
    ):
        if graph is None:
            continue
        oc_attrs = graph.nodes[n_id]

        if oc_attrs["name"] not in ciphers:
            continue

        if a_id := oc_attrs.get("arguments_id"):
            for c_id in filter_ast(graph, a_id, types={"Literal"}):
                a_attrs = graph.nodes[c_id]

                if a_attrs["value_type"] != "number":
                    continue

                if int(a_attrs["value"]) < 2048:
                    yield shard, n_id

        elif oc_attrs["name"] == "RSACryptoServiceProvider":
            yield shard, n_id


def _old_insecure_keys_check(
    shard: GraphShard, ciphers: Set[str]
) -> GraphShardNodes:
    for member in yield_shard_object_creation(shard, ciphers):
        args_list = g.get_ast_childs(shard.graph, member, "argument_list")
        keys = g.get_ast_childs(
            shard.graph, args_list[0], "integer_literal", depth=2
        )
        if keys:
            for key in keys:
                size = int(shard.graph.nodes[key].get("label_text"))
                if size < 2048:
                    yield shard, member
        else:
            object_name = g.match_ast(shard.graph, member)["__1__"]
            if (
                shard.graph.nodes[object_name].get("label_text")
                == "RSACryptoServiceProvider"
            ):
                yield shard, member


def c_sharp_insecure_keys(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    ciphers = {
        "RSACryptoServiceProvider",
        "DSACng",
        "RSACng",
    }

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.CSHARP,
        ):
            if shard.syntax_graph:
                yield from _new_insecure_keys_check(shard, ciphers)
            else:
                yield from _old_insecure_keys_check(shard, ciphers)

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="CSharp"),
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_INSECURE_KEYS,
    )


def c_sharp_rsa_secure_mode(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    name_vars = []

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.CSHARP,
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
                prop = node_to_str(shard.graph, member)
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
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="CSharp"),
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_RSA_SECURE_MODE,
    )


def c_sharp_aesmanaged_secure_mode(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    unsafe_modes = {
        "CipherMode.ECB",
        "CipherMode.OFB",
        "CipherMode.CFB",
    }

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.CSHARP,
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

    def check_props(graph: Graph, match: Dict[str, Optional[str]]) -> bool:
        insecure = False
        props = g.get_ast_childs(
            graph, str(match["__2__"]), "member_access_expression", depth=2
        )

        for prop in props:
            if node_to_str(graph, prop) in unsafe_modes:
                insecure = True

        return insecure

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="CSharp"),
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_AES_SECURE_MODE,
    )


def c_sharp_insecure_cipher(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    c_sharp = GraphShardMetadataLanguage.CSHARP

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

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for member in [
                *yield_syntax_graph_member_access(graph, insecure_ciphers),
                *yield_syntax_graph_object_creation(graph, insecure_ciphers),
            ]:
                yield shard, member

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="CSharp"),
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_INSECURE_CIPHER,
    )


def c_sharp_insecure_hash(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    c_sharp = GraphShardMetadataLanguage.CSHARP

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

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            for member in [
                *yield_shard_member_access(shard, insecure_ciphers),
                *yield_shard_object_creation(shard, insecure_ciphers),
            ]:
                yield shard, member

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params=dict(lang="CSharp"),
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_INSECURE_HASH,
    )


def c_sharp_disabled_strong_crypto(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_DISABLED_STRONG_CRYPTO
    c_sharp = GraphShardMetadataLanguage.CSHARP

    rules = {"Switch.System.Net.DontEnableSchUseStrongCrypto", "true"}

    def n_ids() -> GraphShardNodes:

        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue

            for member in yield_shard_member_access(shard, {"AppContext"}):
                if not check_member_acces_expression(
                    shard, member, "SetSwitch"
                ):
                    continue
                graph = shard.syntax_graph
                pred = g.pred_ast(shard.graph, member)[0]
                for path in get_backward_paths(graph, pred):
                    evaluation = evaluate(method, graph, path, pred)
                    if (
                        evaluation
                        and evaluation.danger
                        and evaluation.triggers == rules
                    ):
                        yield shard, pred

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f052.c_sharp_disabled_strong_crypto",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_obsolete_key_derivation(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_OBSOLETE_KEY_DERIVATION
    c_sharp = GraphShardMetadataLanguage.CSHARP

    def n_ids() -> MetadataGraphShardNodes:
        metadata = {}
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue

            possible_paths = build_attr_paths(
                "System",
                "Security",
                "Cryptography",
                "rfc2898DeriveBytes",
                "CryptDeriveKey",
            )
            s_graph = shard.syntax_graph

            for nid in chain(
                g.filter_nodes(
                    s_graph,
                    s_graph.nodes,
                    g.pred_has_labels(label_type="MethodInvocation"),
                ),
                g.filter_nodes(
                    s_graph,
                    s_graph.nodes,
                    g.pred_has_labels(label_type="ObjectCreation"),
                ),
            ):
                if (
                    s_graph.nodes[nid].get("label_type") == "MethodInvocation"
                    and s_graph.nodes[nid].get("expression") in possible_paths
                ):
                    metadata["desc_params"] = {
                        "expression": s_graph.nodes[nid].get("expression")
                    }
                    yield shard, nid, metadata
                elif (
                    s_graph.nodes[nid].get("label_type") == "ObjectCreation"
                    and s_graph.nodes[nid].get("name") == "PasswordDeriveBytes"
                ):
                    metadata["desc_params"] = {
                        "expression": s_graph.nodes[nid].get("name")
                    }
                    yield shard, nid, metadata

    return get_vulnerabilities_from_n_ids_metadata(
        desc_key="lib_root.f052.c_sharp_obsolete_key_derivation",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
