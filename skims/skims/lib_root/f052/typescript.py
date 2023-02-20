from collections.abc import (
    Iterator,
)
from lib_root.f052.common import (
    insecure_create_cipher,
    insecure_ec_keypair,
    insecure_ecdh_key,
    insecure_encrypt,
    insecure_hash,
    insecure_hash_library,
    insecure_rsa_keypair,
    jwt_insecure_sign,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage,
    GraphShardNode,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)


def ts_insecure_create_cipher(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TS_INSECURE_CREATE_CIPHER

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.TYPESCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in insecure_create_cipher(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def ts_insecure_hash(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TS_INSECURE_HASH

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.TYPESCRIPT
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in insecure_hash(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def ts_insecure_encrypt(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TS_INSECURE_ENCRYPT

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.TYPESCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in insecure_encrypt(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def typescript_insecure_ecdh_key(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TS_INSECURE_ECDH_KEY

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.TYPESCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in insecure_ecdh_key(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.TS_INSECURE_ECDH_KEY,
    )


def typescript_insecure_rsa_keypair(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TS_INSECURE_RSA_KEYPAIR

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.TYPESCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in insecure_rsa_keypair(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def typescript_insecure_ec_keypair(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TS_INSECURE_EC_KEYPAIR

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.TYPESCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in insecure_ec_keypair(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def typescript_insecure_hash_library(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_INSECURE_HASH_LIBRARY

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.TYPESCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in insecure_hash_library(graph):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def typescript_jwt_insec_sign_algorithm(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.TS_JWT_INSEC_SIGN_ALGORITHM

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.TYPESCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in jwt_insecure_sign(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f052.jwt_insecure_signing_algorithm",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
