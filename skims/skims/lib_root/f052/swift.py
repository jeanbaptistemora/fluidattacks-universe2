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


def get_eval_result(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


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


def uses_des_algorithm(graph: Graph, n_id: NId) -> bool:
    named_args = g.match_ast_group_d(graph, n_id, "NamedArgument", 2)
    for arg in named_args:
        arg_name = graph.nodes[arg]["argument_name"]
        val_id = graph.nodes[arg]["value_id"]
        if arg_name == "algorithm" and graph.nodes[val_id]["symbol"] == ".des":
            return True
    return False


def swift_insecure_crypto(
    graph_db: GraphDB,
) -> Vulnerabilities:
    danger_methods = {"Cryptor"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.SWIFT):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in g.matching_nodes(
                graph,
                label_type="MethodInvocation",
            ):
                n_attrs = graph.nodes[n_id]
                ident = n_attrs.get("expression")

                if ident in danger_methods and uses_des_algorithm(graph, n_id):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="Swift"),
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.SWIFT_INSECURE_CRYPTOR,
    )


def swift_insecure_cryptalgo(
    graph_db: GraphDB,
) -> Vulnerabilities:
    danger_methods = {"CryptAlgorithm"}
    method = MethodsEnum.SWIFT_INSECURE_CRYPTOR

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.SWIFT):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in g.matching_nodes(
                graph,
                label_type="MemberAccess",
            ):
                n_attrs = graph.nodes[n_id]
                ident = n_attrs.get("expression")
                parent = g.pred_ast(graph, n_id)[0]
                var_id = graph.nodes[parent]["value_id"]
                if ident in danger_methods and get_eval_result(
                    graph, var_id, method
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="Swift"),
        graph_shard_nodes=n_ids(),
        method=method,
    )
