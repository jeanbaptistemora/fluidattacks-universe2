# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.utilities.go import (
    yield_shard_member_access,
    yield_shard_object_creation,
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
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from typing import (
    Iterable,
)


def go_insecure_hash(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    insecure_ciphers = {"md4", "md5", "ripemd160", "sha1"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.GO):
            for node in yield_shard_object_creation(shard, insecure_ciphers):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params=dict(lang="Go"),
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.GO_INSECURE_HASH,
    )


def go_insecure_cipher(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    insecure_ciphers = {
        "des",
        "NewTripleDESCipher",
    }

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.GO):
            for node in [
                *yield_shard_member_access(shard, insecure_ciphers),
                *yield_shard_object_creation(shard, insecure_ciphers),
            ]:
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="Go"),
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.GO_INSECURE_CIPHER,
    )
