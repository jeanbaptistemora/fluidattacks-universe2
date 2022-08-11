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


def path_injection(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_PATH_INJECTION
    c_sharp = GraphLanguage.CSHARP

    paths = build_attr_paths("System", "IO", "File", "Open")

    def n_ids() -> GraphShardNodes:

        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in search_method_invocation_naive(graph, {"Open"}):
                if (
                    (member := g.match_ast_d(graph, nid, "MemberAccess"))
                    and (expr := graph.nodes[member].get("expression"))
                    and (memb := graph.nodes[member].get("member"))
                    and not (f"{expr}.{memb}" in paths)
                ):
                    continue
                for path in get_backward_paths(graph, nid):
                    if (
                        evaluation := evaluate(method, graph, path, nid)
                    ) and evaluation.danger:
                        yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f098.c_sharp_path_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
