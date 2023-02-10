from itertools import (
    chain,
)
from lib_root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
    yield_syntax_graph_object_creation,
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
    MetadataGraphShardNode,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
    get_vulnerabilities_from_n_ids_metadata,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from typing import (
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
)
import utils.graph as g
from utils.string import (
    build_attr_paths,
)


def get_eval_danger(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def get_eval_triggers(
    graph: Graph,
    n_id: NId,
    method: MethodsEnum,
    rules: Set[str],
) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger and evaluation.triggers == rules:
            return True
    return False


def is_insecure_keys(graph: Graph, n_id: str) -> bool:
    method = MethodsEnum.CS_INSECURE_KEYS
    n_attrs = graph.nodes[n_id]
    unsafe_method = "RSACryptoServiceProvider"

    if n_attrs["name"] == unsafe_method and is_rsa_insecure(graph, n_id):
        return True

    if (
        n_attrs["name"] in {"DSACng", "RSACng"}
        and (a_id := n_attrs.get("arguments_id"))
        and (test_nid := g.match_ast(graph, a_id).get("__0__"))
    ):
        return get_eval_danger(graph, test_nid, method)

    return False


def get_crypto_var_names(
    graph: Graph,
) -> List[NId]:
    name_vars = []
    for var_id in g.matching_nodes(graph, label_type="VariableDeclaration"):
        node_var = graph.nodes[var_id]
        if node_var.get("variable_type") == "RSACryptoServiceProvider":
            name_vars.append(graph.nodes[var_id].get("variable"))
    return name_vars


def get_mode_node(
    graph: Graph,
    members: Tuple[str, ...],
    identifier: str,
) -> Optional[NId]:
    test_node = None
    for member in members:
        if graph.nodes[member].get(identifier) == "Mode":
            test_node = graph.nodes[g.pred(graph, member)[0]].get("value_id")
    return test_node


def is_rsa_insecure(graph: Graph, n_id: NId) -> bool:
    method = MethodsEnum.CS_INSECURE_KEYS
    n_attrs = graph.nodes[n_id]
    a_id = n_attrs.get("arguments_id")

    if not a_id or (
        (test_nid := g.match_ast(graph, a_id).get("__0__"))
        and get_eval_danger(graph, test_nid, method)
    ):
        return True

    return False


def is_managed_mode_insecure(graph: Graph, n_id: NId) -> Optional[NId]:
    method = MethodsEnum.CS_MANAGED_SECURE_MODE

    if g.match_ast_d(graph, n_id, "InitializerExpression"):
        props = g.get_ast_childs(graph, n_id, "SymbolLookup", depth=3)
        test_nid = get_mode_node(graph, props, "symbol")
    else:
        parent_id = g.pred(graph, n_id)[0]
        var_name = graph.nodes[parent_id].get("variable")
        members = [*yield_syntax_graph_member_access(graph, var_name)]
        test_nid = get_mode_node(graph, tuple(members), "member")

    if test_nid and get_eval_danger(graph, test_nid, method):
        return test_nid

    return None


def c_sharp_insecure_keys(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_INSECURE_KEYS

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.CSHARP,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(graph, label_type="ObjectCreation"):
                if is_insecure_keys(graph, n_id):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_rsa_secure_mode(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_RSA_SECURE_MODE

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.CSHARP,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            name_vars = get_crypto_var_names(graph)

            for member in g.matching_nodes(graph, label_type="MemberAccess"):
                n_attrs = graph.nodes[member]
                parent_nid = g.pred(graph, member)[0]

                if (
                    n_attrs["expression"] in name_vars
                    and n_attrs.get("member") == "Encrypt"
                    and (al_id := graph.nodes[parent_nid].get("arguments_id"))
                    and (test_nid := g.match_ast(graph, al_id).get("__1__"))
                    and get_eval_danger(graph, test_nid, method)
                ):
                    yield shard, member

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_managed_secure_mode(
    graph_db: GraphDB,
) -> Vulnerabilities:
    insecure_objects = {"AesManaged"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.CSHARP,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in g.matching_nodes(graph, label_type="ObjectCreation"):
                if graph.nodes[nid].get("name") in insecure_objects and (
                    mode_nid := is_managed_mode_insecure(graph, nid)
                ):
                    yield shard, mode_nid

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_MANAGED_SECURE_MODE,
    )


def c_sharp_insecure_cipher(
    graph_db: GraphDB,
) -> Vulnerabilities:
    c_sharp = GraphShardMetadataLanguage.CSHARP
    insecure_ciphers = {
        "AesFastEngine",
        "DES",
        "DESCryptoServiceProvider",
        "DesEdeEngine",
        "DSACryptoServiceProvider",
        "RC2",
        "RC2CryptoServiceProvider",
        "RijndaelManaged",
        "TripleDES",
        "TripleDESCng",
        "TripleDESCryptoServiceProvider",
        "Blowfish",
    }

    def n_ids() -> Iterable[GraphShardNode]:
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
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_INSECURE_CIPHER,
    )


def c_sharp_insecure_hash(
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

    def n_ids() -> Iterable[GraphShardNode]:
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
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_INSECURE_HASH,
    )


def c_sharp_disabled_strong_crypto(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_DISABLED_STRONG_CRYPTO
    c_sharp = GraphShardMetadataLanguage.CSHARP
    rules = {"Switch.System.Net.DontEnableSchUseStrongCrypto", "true"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for member in yield_syntax_graph_member_access(
                graph, {"AppContext"}
            ):
                test_nid = g.pred_ast(graph, member)[0]
                if graph.nodes[member][
                    "member"
                ] == "SetSwitch" and get_eval_triggers(
                    graph, test_nid, method, rules
                ):
                    yield shard, test_nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f052.c_sharp_disabled_strong_crypto",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_obsolete_key_derivation(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_OBSOLETE_KEY_DERIVATION
    c_sharp = GraphShardMetadataLanguage.CSHARP
    possible_paths = build_attr_paths(
        "System",
        "Security",
        "Cryptography",
        "rfc2898DeriveBytes",
        "CryptDeriveKey",
    )

    def n_ids() -> Iterable[MetadataGraphShardNode]:
        metadata = {}
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in chain(
                g.matching_nodes(graph, label_type="MethodInvocation"),
                g.matching_nodes(graph, label_type="ObjectCreation"),
            ):
                n_attrs = graph.nodes[nid]
                if (
                    n_attrs["label_type"] == "MethodInvocation"
                    and (expr := n_attrs.get("expression"))
                    and expr in possible_paths
                ):
                    metadata["desc_params"] = {"expression": expr}
                    yield shard, nid, metadata
                elif (
                    n_attrs["label_type"] == "ObjectCreation"
                    and n_attrs.get("name") == "PasswordDeriveBytes"
                ):
                    metadata["desc_params"] = {"expression": n_attrs["name"]}
                    yield shard, nid, metadata

    return get_vulnerabilities_from_n_ids_metadata(
        desc_key="lib_root.f052.c_sharp_obsolete_key_derivation",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
