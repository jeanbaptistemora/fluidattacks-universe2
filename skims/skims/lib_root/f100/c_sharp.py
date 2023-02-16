from collections.abc import (
    Iterator,
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
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)
from utils.string import (
    build_attr_paths,
)


def is_insecure_create(graph: Graph, member: NId, nid: NId) -> bool:
    method = MethodsEnum.CS_INSEC_CREATE
    paths = build_attr_paths("System", "Net", "WebRequest", "Create")
    expr = graph.nodes[member].get("expression")
    memb = graph.nodes[member].get("member")

    if expr and memb and f"{expr}.{memb}" in paths:
        for path in get_backward_paths(graph, nid):
            evaluation = evaluate(method, graph, path, nid)
            if evaluation and evaluation.danger:
                return True
    return False


def insec_create(
    graph_db: GraphDB,
) -> Vulnerabilities:
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in search_method_invocation_naive(graph, {"Create"}):
                if (
                    member := g.match_ast_d(graph, n_id, "MemberAccess")
                ) and is_insecure_create(graph, member, n_id):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f100.insec_create.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_INSEC_CREATE,
    )
