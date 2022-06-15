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
from utils.graph.text_nodes import (
    node_to_str,
)
from utils.string import (
    build_attr_paths,
)


def insec_create(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.SYMB_INSEC_CREATE
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue

            paths = build_attr_paths("System", "Net", "WebRequest", "Create")

            graph = shard.syntax_graph
            for n_id in search_method_invocation_naive(graph, {"Create"}):
                if (
                    member := g.match_ast_d(
                        shard.graph, n_id, "member_access_expression"
                    )
                ) and not node_to_str(shard.graph, member) in paths:
                    continue
                for path in get_backward_paths(graph, n_id):
                    if (
                        evaluation := evaluate(method, graph, path, n_id)
                    ) and evaluation.danger:
                        yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f100.insec_create.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
