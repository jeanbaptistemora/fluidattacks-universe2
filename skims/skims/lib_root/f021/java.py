from collections.abc import (
    Iterator,
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
from utils import (
    graph as g,
)


def unsafe_xpath_injeciton(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.JAVA_XPATH_INJECTION_EVALUATE
    danger_methods = {"evaluate"}
    danger_set = {"userparameters", "userconnection"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.JAVA):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
                n_attrs = graph.nodes[n_id]
                if n_attrs[
                    "expression"
                ] in danger_methods and get_node_evaluation_results(
                    method, graph, n_id, danger_set, False
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f021.xpath_injection_evaluate",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
