from lib_root.utilities.c_sharp import (
    get_first_member_syntax_graph,
)
from lib_root.utilities.common import (
    search_method_invocation_naive,
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
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
    get_object_identifiers,
)
from typing import (
    Iterable,
)


def get_eval_danger(graph: Graph, n_id: str, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def is_insec_input(graph: Graph, n_id: str, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.triggers == {
            "userconnection",
        }:
            return True
    return False


def xpath_injection(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_XPATH_INJECTION
    c_sharp = GraphLanguage.CSHARP
    danger_meths = {"SelectSingleNode"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            xpath_obj = get_object_identifiers(graph, {"XPathNavigator"})

            for n_id in search_method_invocation_naive(graph, danger_meths):
                if (
                    (memb := get_first_member_syntax_graph(graph, n_id))
                    and graph.nodes[memb].get("symbol") in xpath_obj
                    and get_eval_danger(graph, n_id, method)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f021.xpath_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def xpath_injection_evaluate(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_XPATH_INJECTION_EVALUATE
    c_sharp = GraphLanguage.CSHARP
    danger_meths = {"Evaluate"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in search_method_invocation_naive(graph, danger_meths):
                if is_insec_input(graph, n_id, method):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f021.xpath_injection_evaluate",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
