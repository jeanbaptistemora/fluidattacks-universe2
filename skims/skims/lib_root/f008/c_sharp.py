from collections.abc import (
    Iterator,
    Set,
)
from itertools import (
    chain,
)
from lib_root.utilities.common import (
    search_method_invocation_naive,
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
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)


def search_member_accessed(graph: Graph, members: Set[str]) -> Iterator[NId]:
    for nid in g.matching_nodes(graph, label_type="MemberAccess"):
        if (
            graph.nodes[nid].get("member") in members
            and (parent := g.pred_ast(graph, nid)[0])
            and graph.nodes[parent]["label_type"] == "Assignment"
        ):
            yield parent


def insec_addheader_write(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.CS_INSEC_ADDHEADER_WRITE
    danger_methods = {"AddHeader", "Write"}
    danger_members = {"StatusDescription"}
    danger_set = {"userconnection", "userparams"}

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in chain(
                search_method_invocation_naive(graph, danger_methods),
                search_member_accessed(graph, danger_members),
            ):
                if get_node_evaluation_results(
                    method, graph, n_id, danger_set
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f008.insec_addheader_write.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
