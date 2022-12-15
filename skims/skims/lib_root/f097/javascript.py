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
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from typing import (
    Iterable,
    List,
)
from utils import (
    graph as g,
)


def has_dangerous_param(graph: Graph) -> List[NId]:
    vuln_nodes: List[NId] = []

    for n_id in g.filter_nodes(
        graph,
        graph.nodes,
        g.pred_has_labels(label_type="MethodInvocation"),
    ):
        vuln_nodes.append(n_id)

    return vuln_nodes


def has_reverse_tabnabbing(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_HAS_REVERSE_TABNABBING

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in has_dangerous_param(graph):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f097.has_reverse_tabnabbing",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
