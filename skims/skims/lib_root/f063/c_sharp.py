from lib_root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
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


def open_redirect(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_OPEN_REDIRECT
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> GraphShardNodes:

        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue

            graph = shard.syntax_graph

            for member in yield_syntax_graph_member_access(
                graph, {"Response"}
            ):
                if not graph.nodes[member].get("member") == "Redirect":
                    continue
                pred = g.pred_ast(graph, member)[0]
                for path in get_backward_paths(graph, pred):
                    if (
                        evaluation := evaluate(method, graph, path, pred)
                    ) and evaluation.danger:
                        yield shard, pred

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f063.c_sharp_open_redirect",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
