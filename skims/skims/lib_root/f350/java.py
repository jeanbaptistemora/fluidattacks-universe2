from collections.abc import (
    Iterator,
)
from lib_root.utilities.java import (
    yield_method_invocation_syntax_graph,
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


def eval_trust_manager(graph: Graph, n_id: NId) -> bool:
    method = MethodsEnum.JAVA_INSECURE_TRUST_MANAGER
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def use_insecure_trust_manager(
    graph_db: GraphDB,
) -> Vulnerabilities:
    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for m_id, m_name in yield_method_invocation_syntax_graph(graph):
                m_split = m_name.lower().split(".")
                if (
                    m_split[0] == "sslcontextbuilder"
                    and m_split[-1] == "trustmanager"
                    and eval_trust_manager(graph, m_id)
                ):
                    yield shard, m_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f350.insecure_trust_manager",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_INSECURE_TRUST_MANAGER,
    )
