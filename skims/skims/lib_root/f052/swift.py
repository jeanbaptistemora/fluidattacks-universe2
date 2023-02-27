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
import utils.graph as g


def get_all_imports(graph: Graph) -> list[str]:
    return [
        graph.nodes[n_id]["expression"]
        for n_id in g.matching_nodes(
            graph,
            label_type="Import",
        )
    ]


def cc_algorithms(
    graph: Graph, ident: str, n_id: NId, file_imports: list[str]
) -> bool:
    if (
        ident == "CCAlgorithm"
        and "CommonCrypto" in file_imports
        and (args_id := graph.nodes[n_id].get("arguments_id"))
    ):
        arg = g.match_ast_d(graph, args_id, "SymbolLookup", 2)
        if graph.nodes[arg]["symbol"] == "kCCAlgorithmDES":
            return True
    return False


def swift_insecure_cipher(
    graph_db: GraphDB,
) -> Vulnerabilities:
    danger_methods = {
        ("Blowfish", "CryptoSwift"),
        (
            ".des",
            "IDZSwiftCommonCrypto",
        ),
    }

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.SWIFT):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            file_imports = get_all_imports(graph)
            for n_id in [
                *g.matching_nodes(
                    graph,
                    label_type="MethodInvocation",
                ),
                *g.matching_nodes(
                    graph,
                    label_type="SymbolLookup",
                ),
            ]:
                n_attrs = graph.nodes[n_id]
                ident = n_attrs.get("expression") or n_attrs.get("symbol")

                if any(
                    meth == ident and imp in file_imports
                    for meth, imp in danger_methods
                ) or cc_algorithms(graph, ident, n_id, file_imports):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="Swift"),
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.SWIFT_INSECURE_CIPHER,
    )
