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
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNodes,
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


def insecure_assembly_load(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_INSECURE_ASSEMBLY_LOAD
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> GraphShardNodes:

        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue

            paths = build_attr_paths(
                "System", "Reflection", "Assembly", "Load"
            )
            graph = shard.syntax_graph

            for n_id in search_method_invocation_naive(graph, {"Load"}):
                if (
                    (member := g.match_ast_d(graph, n_id, "MemberAccess"))
                    and (expr := graph.nodes[member].get("expression"))
                    and (memb := graph.nodes[member].get("member"))
                    and (f"{expr}.{memb}" not in paths)
                ):
                    continue
                for path in get_backward_paths(graph, n_id):
                    if (
                        evaluation := evaluate(method, graph, path, n_id)
                    ) and evaluation.danger:
                        yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f413.insecure_assembly_load",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
