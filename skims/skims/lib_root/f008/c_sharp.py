from itertools import (
    chain,
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
    Iterator,
    Set,
)
from utils import (
    graph as g,
)


def is_insec_header(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    danger_set = {"userconnection", "userparams"}
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if (
            evaluation
            and evaluation.danger
            and evaluation.triggers == danger_set
        ):
            return True
    return False


def search_member_accessed(graph: Graph, members: Set[str]) -> Iterator[NId]:
    for nid in g.filter_nodes(
        graph,
        nodes=graph.nodes,
        predicate=g.pred_has_labels(label_type="MemberAccess"),
    ):
        if (
            graph.nodes[nid].get("member") in members
            and (parent := g.pred_ast(graph, nid)[0])
            and graph.nodes[parent]["label_type"] == "Assignment"
        ):
            yield parent


def insec_addheader_write(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_INSEC_ADDHEADER_WRITE
    c_sharp = GraphLanguage.CSHARP
    danger_methods = {"AddHeader", "Write"}
    danger_members = {"StatusDescription"}

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in chain(
                search_method_invocation_naive(graph, danger_methods),
                search_member_accessed(graph, danger_members),
            ):
                if is_insec_header(graph, n_id, method):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f008.insec_addheader_write.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
