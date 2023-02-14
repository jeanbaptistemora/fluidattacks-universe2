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
from typing import (
    Iterable,
    List,
)
from utils import (
    graph as g,
)


def is_salt_harcoded(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def has_dangerous_param(graph: Graph, method: MethodsEnum) -> List[NId]:
    vuln_nodes: List[NId] = []
    sensitive_methods = {"salt", "SALT"}

    for n_id in g.matching_nodes(graph, label_type="SymbolLookup"):
        if graph.nodes[n_id].get("symbol") in sensitive_methods:
            if is_salt_harcoded(graph, n_id, method):
                vuln_nodes.append(n_id)

    return vuln_nodes


def java_salting_is_harcoded(
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_SALT_IS_HARDCODED

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in has_dangerous_param(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f338.salt_is_hardcoded",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
