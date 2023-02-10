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
import utils.graph as g


def go_insecure_hash(
    graph_db: GraphDB,
) -> Vulnerabilities:
    danger_methods = {"md4", "md5", "ripemd160", "sha1"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.GO):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(
                graph,
                label_type="MemberAccess",
            ):
                n_attrs = graph.nodes[n_id]
                if (
                    n_attrs["member"] in danger_methods
                    and n_attrs["expression"] == "New"
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params=dict(lang="Go"),
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.GO_INSECURE_HASH,
    )


def go_insecure_cipher(
    graph_db: GraphDB,
) -> Vulnerabilities:
    danger_methods = {"des.NewTripleDESCipher", "blowfish.NewCipher"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.GO):
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
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="Go"),
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.GO_INSECURE_CIPHER,
    )
