from collections.abc import (
    Iterator,
)
from lib_root.utilities.c_sharp import (
    get_first_member_syntax_graph,
)
from lib_root.utilities.common import (
    search_method_invocation_naive,
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
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from symbolic_eval.utils import (
    get_object_identifiers,
)


def xpath_injection(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.CS_XPATH_INJECTION
    danger_meths = {"SelectSingleNode"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            xpath_obj = get_object_identifiers(graph, {"XPathNavigator"})

            for n_id in search_method_invocation_naive(graph, danger_meths):
                if (
                    (memb := get_first_member_syntax_graph(graph, n_id))
                    and graph.nodes[memb].get("symbol") in xpath_obj
                    and get_node_evaluation_results(method, graph, n_id, set())
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f021.xpath_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def xpath_injection_evaluate(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.CS_XPATH_INJECTION_EVALUATE
    danger_meths = {"Evaluate"}
    danger_set = {"userconnection"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in search_method_invocation_naive(graph, danger_meths):
                if get_node_evaluation_results(
                    method, graph, n_id, danger_set, False
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f021.xpath_injection_evaluate",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
