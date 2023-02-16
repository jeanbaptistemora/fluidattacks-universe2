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


def eval_insecure_xaml(graph: Graph, n_id: NId) -> bool:
    method = MethodsEnum.CS_XAML_INJECTION
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def xaml_injection(
    graph_db: GraphDB,
) -> Vulnerabilities:
    c_sharp = GraphLanguage.CSHARP
    paths = build_attr_paths(
        "System", "Windows", "Markup", "XamlReader", "Load"
    )

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in search_method_invocation_naive(graph, {"Load"}):
                if (
                    (member := g.match_ast_d(graph, n_id, "MemberAccess"))
                    and (expr := graph.nodes[member].get("expression"))
                    and (memb := graph.nodes[member].get("member"))
                    and (f"{expr}.{memb}" in paths)
                    and eval_insecure_xaml(graph, n_id)
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f416.xaml_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_XAML_INJECTION,
    )
